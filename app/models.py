from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
TAGS = [
    {'id': 1, 'name': 'django'},
    {'id': 2, 'name': 'python'},
    {'id': 3, 'name': 'HTML'},
]

QUESTIONS = [
    {'id': i + 1,
     'title': 'Как создать приложение? ' + str(i + 1),
     'text': 'Мой вопрос заключается в том, что мне необходимо сделать кое-что интересное. '
             'Я думаю над тем, как создать собственное веб-приложение. Не могли бы вы'
             'посоветовать, какие технологии мне нужно изучить и с каких языков '
             'программирования начать?',
     'answers': 10,
     'likes': 5,
     'tags': [TAGS[0], TAGS[1], TAGS[2]],
     'user': 1,
     'date': 'DD.MM.YYYY HH:MM'} for i in range(15)
]

USERS = [
    {'id': i + 1,
     'login': 'userxxx',
     'email': 'user2000@mail.ru',
     'password': '12345',
     'avatar': 'file.txt',
     'firstname': 'Firstname',
     'lastname': 'Lastname'} for i in range(3)
]

ANSWERS = [
    {'id': i + 1,
     'text': 'Во-первых, тебе необходимо начать изучать этот фраемворк, а также изучить данную технологию. '
             'Тебе будет легко сделать шаблонный пример, но над чем-то своим тебе придётся долго и упорно '
             'работать. Желаю удачи!',
     'likes': 5,
     'user': 2,
     'best_answer': 0,
     'question': 1,
     'date': 'DD.MM.YYYY HH:MM'} for i in range(13)
]

COOKIES = [
    {'user': '1'}
]


class QuestionsQuerySet(models.QuerySet):
    def get_full_form(self):
        return self.annotate(likes=Count('q_likes', distinct=True), answer_cnt=Count('q_answers', distinct=True))

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


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    question_list = QuestionsManager()


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()
    best_answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers',
                                 related_query_name='q_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes',
                                 related_query_name='q_likes')


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes',
                               related_query_name='a_likes')


class QuestionTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_tags',
                                 related_query_name='q_tags')
