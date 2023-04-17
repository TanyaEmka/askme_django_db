from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class QuestionsQuerySet(models.QuerySet):
    def get_full_form(self):
        return self.annotate(likes=Count('all_likes', distinct=True), answer_cnt=Count('q_answers', distinct=True))

    def new_questions(self):
        context_queryset = self.get_full_form()
        return context_queryset.order_by('-date')

    def best_questions(self):
        context_queryset = self.get_full_form()
        return context_queryset.order_by('-likes')

    def tag_questions(self, tag_name):
        context_queryset = self.get_full_form()
        return context_queryset.filter(q_tags__tag__name=tag_name).order_by('-date')


class QuestionsManager(models.Manager):
    def get_queryset(self):
        return QuestionsQuerySet(self.model)

    def new_questions(self):
        return self.get_queryset().new_questions()

    def best_questions(self):
        return self.get_queryset().best_questions()

    def tag_questions(self, tag_name):
        return self.get_queryset().tag_questions(tag_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)

    objects = models.Manager()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id',)


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_likes = GenericRelation(Like, related_name='all_likes')

    objects = models.Manager()
    question_list = QuestionsManager()


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    best_answer = models.BooleanField(default=False, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers',
                                 related_query_name='q_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_likes = GenericRelation(Like, related_name='all_likes')

    @property
    def likes(self):
        return self.all_likes.count()


class QuestionTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_tags',
                                 related_query_name='q_tags')
