"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.questions_page, name='questions'),
    path('best/', views.best_questions_page, name='best_questions'),
    path('question/<int:question_id>/', views.question_page, name='question'),
    path('new_question/', views.new_question, name='new_question'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('user/', views.user_page, name='user'),
    path('edit_user/', views.user_edit_view, name='edit_user'),
    path('tag/<str:tag>/', views.tag_questions, name='tag'),
    path('logout/', views.logout_view, name='logout'),
]
