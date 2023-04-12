from django.core.management.base import BaseCommand
from app.models import Question, Tag, Profile, Answer, QuestionTags, Like, AnswerLike
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fill database'

    def handle(self, *args, **options):
        base_tags = ['python', 'django', 'HTML', 'css', 'Typescript', 'javascript', 'go', 'C', 'C++', 'mysql']
        base_user = ['New_user', 'Firstname', 'Lastname', 'newuser@mail.ru', 'a1a2a3a4']
        admin_u = User.objects.get(pk=1)
        for i in range(options['ratio']):
            index = ""
            if i != 0:
                index = str(i)
            t = Tag(name=base_tags[i % len(base_tags)] + index)
            u = User(username=base_user[0] + index,
                     first_name=base_user[1] + index,
                     last_name=base_user[2] + index,
                     email=index + base_user[3],
                     password=index + base_user[4])
            p = Profile(user=u, avatar=None)
            t.save()
            u.save()
            p.save()
            for j in range(10):
                index_j = ""
                if j != 0:
                    index_j = str(j)
                q = Question(title='Как создать приложение?' + index + '-' + index_j,
                             text='Мой вопрос заключается в том, что мне необходимо сделать кое-что интересное. '
                                  'Я думаю над тем, как создать собственное веб-приложение. Не могли бы вы'
                                  'посоветовать, какие технологии мне нужно изучить и с каких языков '
                                  'программирования начать? ' + index + '-' + index_j,
                             date=timezone.now(),
                             user=u)
                qt = QuestionTags(tag=t, question=q)
                q.save()
                qt.save()
                for k in range(10):
                    index_k = ""
                    if k != 0:
                        index_k = str(k)
                    a = Answer(text='Во-первых, тебе необходимо начать изучать этот фраемворк, а также изучить данную '
                                    'технологию. '
                                    'Тебе будет легко сделать шаблонный пример, но над чем-то своим тебе придётся '
                                    'долго и упорно '
                                    'работать. Желаю удачи!' + index + '-' + index_j + '-' + index_k,
                               date=timezone.now(),
                               best_answer=False,
                               question=q,
                               user=u)
                    al = AnswerLike(user=u, answer=a)
                    al2 = AnswerLike(user=admin_u, answer=a)
                    a.save()
                    al.save()
                    al2.save()
        print('End process')

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio',
            nargs='?',
            type=int,
        )
