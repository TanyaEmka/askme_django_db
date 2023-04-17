from django.shortcuts import render
from app import models
from app import functions
from django.db.models import Count


# Create your views here.
def tag_questions(request, tag):
    try:
        full_tag = models.Tag.objects.get(name=tag)
    except:
        full_tag = {'pk': 0, 'name': 'ошибка'}
    context_questions = models.Question.question_list.tag_questions(tag).all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'tag': full_tag,
        'full_count': context_questions.count()
    }}
    return render(request, 'tag_questions.html', context)


def questions_page(request):
    context_questions = models.Question.question_list.new_questions().all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'full_count': context_questions.count()
    }}
    return render(request, 'index.html', context)


def best_questions_page(request):
    context_questions = models.Question.question_list.best_questions().all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'full_count': context_questions.count()
    }}
    return render(request, 'best_questions.html', context)


def question_page(request, question_id):
    context_question = models.Question.question_list.new_questions().get(pk=question_id)
    context_answers = context_question.question_answers.all()
    context = {'data': {
        'question': context_question,
        'answers': functions.get_page_data(context_answers, 5, request.GET.get('page')),
        'full_count': context_answers.count()
    }}
    return render(request, 'question_page.html', context)


def new_question(request):
    return render(request, 'new_question.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def user_page(request):
    return render(request, 'user_page.html')
