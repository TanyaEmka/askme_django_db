from django.core.management.base import BaseCommand
from app.models import Question, Tag, Profile, Answer, Like
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Fill database'

    def handle(self, *args, **options):
        base_tags = ['python', 'django', 'HTML', 'css', 'Typescript', 'javascript', 'go', 'C', 'C++', 'mysql']
        base_user = ['New_user', 'Firstname', 'Lastname', 'newuser@mail.ru', 'a1a2a3a4']
        question_id = 1
        answer_id = 1
        for i in range(options['ratio']):
            index = ""
            if i != 0:
                index = str(i)
            t = Tag(name=base_tags[i % len(base_tags)] + index)
            u = User(username=base_user[0] + index,
                     first_name=base_user[1] + index,
                     last_name=base_user[2] + index,
                     email=index + base_user[3],
                     password=make_password(index + base_user[4]))
            p = Profile(user=u, avatar=None)
            t.save()
            u.save()
            p.save()
            for j in range(10):
                index_j = ""
                if j != 0:
                    index_j = str(j)
                q = Question.objects.create_question(title='Как создать приложение?' + index + '-' + index_j,
                             text='Мой вопрос заключается в том, что мне необходимо сделать кое-что интересное. '
                                  'Я думаю над тем, как создать собственное веб-приложение. Не могли бы вы'
                                  'посоветовать, какие технологии мне нужно изучить и с каких языков '
                                  'программирования начать? ' + index + '-' + index_j,
                             user=u, tags=[t])
                q.save()
                like = Like.objects.create_like(user=u, instance=q, object_id=q.id)
                question_id += 1
                like.save()
                for k in range(10):
                    index_k = ""
                    if k != 0:
                        index_k = str(k)
                    a = Answer.objects.create_answer(
                                text='Во-первых, тебе необходимо начать изучать этот фраемворк, а также изучить данную '
                                    'технологию. '
                                    'Тебе будет легко сделать шаблонный пример, но над чем-то своим тебе придётся '
                                    'долго и упорно '
                                    'работать. Желаю удачи!' + index + '-' + index_j + '-' + index_k,
                               question=q,
                               user=u)
                    a.save()
                    if j != 9:
                        al = Like(user=u, content_type=ContentType.objects.get_for_model(a), object_id=answer_id)
                        al.save()
                    answer_id += 1
        for i in range(options['ratio']):
            if i != options['ratio'] - 1:
                current_u = User.objects.get(pk=i + 2)  # т.к. нужно учитывать админа
            else:
                current_u = User.objects.get(pk=1)  # т.к. нужно учитывать админа
            for j in range(5):
                q_index = 10 * i + j + 1
                q = Question.objects.get(pk=q_index)
                like = Like.objects.create_like(user=current_u, instance=q, object_id=q.id)
                like.save()
            for k in range(95):
                a_index = 100 * i + k + 1
                a = Answer.objects.get(pk=a_index)
                al = Like.objects.create_like(user=current_u, instance=a, object_id=a.id)
                al.save()
        print('End process')

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio',
            nargs='?',
            type=int,
        )
