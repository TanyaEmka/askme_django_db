from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from generic_aggregation import generic_aggregate, generic_annotate


# Create your models here.
def user_directory_path(instance, filename):
    return 'user{0}/{1}'.format(instance.user.id, filename)


class LikeManager(models.Manager):
    def is_my_like(self, user, object_id):
        try:
            like = self.filter(user=user).get(object_id=object_id)
            if like.is_active:
                return True
        except Like.DoesNotExist:
            pass
        return False

    def create_like(self, user, instance, object_id, action='up-vote'):
        try:
            like = self.filter(user=user).get(object_id=object_id)
            if like.is_active and action == 'down-vote':
                like.is_active = False
                instance.all_likes -= 1
            elif not like.is_active and action == 'up-vote':
                like.is_active = True
                instance.all_likes += 1
            like.save(update_fileds=['is_active'])
        except:
            like = self.create(user=user, content_object=instance, object_id=instance.id)
            if action == 'up-vote':
                instance.all_likes += 1
            else:
                like.is_active = False
            like.save()
        instance.save(update_fields=['all_likes'])
        return like


class ProfileManager(models.Manager):
    @staticmethod
    def update_profile_and_user(user, cleaned_data):
        user_fields = ['username', 'email', 'first_name', 'last_name']
        profile_fields = ['avatar']
        fields_for_update = {'user': [], 'profile': []}
        try:
            profile = Profile.objects.get(user=user.id)
            for element in profile_fields:
                value = cleaned_data.get(element, False)
                if value:
                    fields_for_update['profile'].append(value)
                    setattr(profile, element, value)
            profile.save(update_fields=fields_for_update['profile'])
        except:
            pass
        user = User.objects.get(pk=user.id)
        for element in user_fields:
            value = cleaned_data.get(element, False)
            if value:
                fields_for_update['user'].append(value)
                setattr(user, element, value)

        user.save()
        return user


class TagManager(models.Manager):
    def create_or_update_tag(self, tag):
        try:
            tag = self.get(name=tag)
            tag.tag_count += 1
            tag.save(update_fields=['tag_count'])
        except Tag.DoesNotExist:
            tag = self.create(name=tag, tag_count=1)
            tag.save()
        return tag


class QuestionsQuerySet(models.QuerySet):
    def new_questions(self):
        return self.order_by('-date')

    def best_questions(self):
        return self.order_by('-all_likes')

    def tag_questions(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-date')


class QuestionsManager(models.Manager):
    def get_queryset(self):
        return QuestionsQuerySet(self.model)

    def new_questions(self):
        return self.get_queryset().new_questions()

    def best_questions(self):
        return self.get_queryset().best_questions()

    def tag_questions(self, tag_name):
        return self.get_queryset().tag_questions(tag_name)

    def create_question(self, **kwargs):
        user_id = kwargs['user']
        title = kwargs['title']
        text = kwargs['text']
        tags = kwargs['tags']
        print(tags)
        question = self.create(user=user_id, title=title, text=text)
        question.save()
        for tag in tags:
            curr_tag = Tag.objects.create_or_update_tag(tag)
            curr_tag.save()
            question.tags.add(curr_tag)
        return question


class AnswerManager(models.Manager):
    def create_answer(self, user, question, text, all_likes=0):
        answer = self.create(user=user, question=question, text=text, all_likes=all_likes)
        question = Question.objects.get(pk=question.id)
        question.all_answers += 1
        question.save(update_fields=['all_answers'])

        return answer


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to=user_directory_path, default="avatar.svg")

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tag_count = models.IntegerField(default=1)

    objects = TagManager()

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeManager()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id',)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_likes = models.IntegerField(default=0)
    all_answers = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    objects = QuestionsManager()


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    best_answer = models.BooleanField(default=False, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers',
                                 related_query_name='q_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_likes = models.IntegerField(default=0)

    objects = AnswerManager()

    def __str__(self):
        return self.question.title
