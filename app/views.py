from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
import math


from django.shortcuts import render
from app import models
from app import functions
from app import forms
from django.db.models import Count


# Create your views here.
def tag_questions(request, tag):
    try:
        full_tag = models.Tag.objects.get(name=tag)
    except:
        full_tag = {'pk': 0, 'name': 'ошибка'}
    context_questions = models.Question.objects.tag_questions(tag).all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'tag': full_tag,
        'full_count': context_questions.count()
    }}
    return render(request, 'tag_questions.html', context)


def questions_page(request):
    context_questions = models.Question.objects.new_questions().all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'full_count': context_questions.count()
    }}
    return render(request, 'index.html', context)


def best_questions_page(request):
    context_questions = models.Question.objects.best_questions().all()
    context = {'data': {
        'questions': functions.get_page_data(context_questions, 10, request.GET.get('page')),
        'full_count': context_questions.count()
    }}
    return render(request, 'best_questions.html', context)


def question_page(request, question_id):
    context_question = models.Question.objects.new_questions().get(pk=question_id)
    context = {}
    page_number = 1

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.create_answer(user=request.user, question=context_question, text=form.cleaned_data['text'])
            answer.save()
            context_answers_cnt = context_question.question_answers.all().count()
            page_number = math.ceil(int(context_answers_cnt / 5)) + 1
            if page_number != 1:
                return redirect('./?page=' + str(page_number))
            else:
                return redirect('.')
        else:
            context.update({'error': "Invalid answer's data"})

    if context_question is None:
        raise Http404

    context_answers = context_question.question_answers.all()
    form = forms.AnswerForm()
    context.update({'data': {
        'question': context_question,
        'answers': functions.get_page_data(context_answers, 5, request.GET.get('page')),
        'full_count': context_answers.count(),
        'form': form,
    }})
    return render(request, 'question_page.html', context)


@login_required(login_url='/login')
def new_question(request):
    if request.method == 'POST':
        title = request.POST['title']
        tags = request.POST['tags'].split(',')
        text = request.POST['text']
        question = models.Question.objects.create_question(user=request.user, title=title, tags=tags, text=text)
        if question is not None:
            question.save()
            return redirect('../question/{}'.format(question.id))
        return render(request, 'new_question.html', {'error': 'Something went wrong. Try again.'})
    return render(request, 'new_question.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            path = "/user"
            if request.GET.get("next"):
                path = request.GET.get("next")
            return redirect(path)
        return render(request, 'login.html', {
            'error': 'Login or/and password are incorrect. Try again.'
        })
    return render(request, 'login.html')


@transaction.atomic()
def registration(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        context = {'form': form}
        if not form.is_valid():
            return render(request, 'registration.html', context=context)

        username, email, password = form['username'].value(), form['email'].value(), form['password'].value()

        if User.objects.filter(username=username).exists():
            context.update({'error': 'Login "{}" already taken.'.format(username)})
            return render(request, 'registration.html', context=context)

        if User.objects.filter(email=email).exists():
            context.update({'error': 'Email "{}" already taken.'.format(email)})
            return render(request, 'registration.html', context=context)

        if form['password'].value() != form['repeated_password'].value():
            context.update({'error': 'Passwords are not the same.'})
            return render(request, 'registration.html', context={'error': 'Passwords are not the same.'})

        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=form['first_name'].value(),
                                        last_name=form['last_name'].value())
        if user is not None:
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user')
            return redirect('questions')
        else:
            context.update({'error': 'Server error. Try again.'})
            return render(request, 'registration.html', context=context)

    return render(request, 'registration.html', context={'form': forms.RegistrationForm()})


@login_required(login_url='/login/')
def user_page(request):
    user = request.user
    return render(request, 'user_page.html',
                  {'user': user})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('questions')


@login_required(login_url='/login')
def user_edit_view(request):
    context = {}
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            context.update({'error': 'Something wrond with data', 'form': forms.EditProfileForm()})
            return render(request, 'user_edit.html', context=context)

        user = request.user
        models.Profile.objects.update_profile_and_user(user, form.cleaned_data)
        return redirect('/user')
    form = forms.EditProfileForm()
    context.update({'form': form})
    return render(request, 'user_edit.html', context=context)
