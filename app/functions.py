from app import models
from django.core.paginator import Paginator


def get_page_data(data, page_count, page_number):
    paginator = Paginator(data, page_count)
    if page_number is None:
        page_number = 1
    return paginator.get_page(page_number)


def get_tag_questions(questions, tag_id):
    need_questions = []
    for question in questions:
        for tag in question['tags']:
            if tag['id'] == tag_id:
                need_questions.append(question)
    return need_questions


def get_tag_by_name(tag_name):
    need_tag = {}
    for tag in models.TAGS:
        if tag['name'] == tag_name:
            need_tag = tag
            return need_tag
    return need_tag
