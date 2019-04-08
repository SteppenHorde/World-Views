from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models.news import *
from polls.models.polls import *
from tests.models.tests import *
from core.models.news import *

from collections import OrderedDict



def main(request):
    latest_polls_list = PollsPoll.objects.filter(published=True).order_by('-pub_date')[:2]
    latest_polls = OrderedDict()
    completed_polls = set()
    selected_choices = request.session.get('selected_choices', list())
    for poll in latest_polls_list:
        choices = PollsChoice.objects.filter(question=poll)
        if set(selected_choices) & set((choice.id for choice in choices)): # & - пересечение
            completed_polls.add(poll.id)
        latest_polls[poll] = choices

    latest_tests = TestsTest.objects.filter(published=True).order_by('-pub_date')[:2]
    latest_news = News.objects.filter(published=True).order_by('-pub_date')[:2]
    context = {
        'polls':latest_polls,
        'tests':latest_tests,
        'news_list':latest_news,
        'selected_choices':selected_choices,
        'completed_polls':completed_polls,
        }

    return render(request, 'core/main.html', context=context)


def news(request):
    news_list = News.objects.filter(published=True).order_by('-pub_date')
    context = {
        'news_list': news_list,
        }

    return render(request, 'core/news.html', context=context)


def show_news(request, news_id):
    try:
        news = News.objects.get(
            Q(published=True) & Q(pk=news_id)
            )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    context = {
        'news': news,
        }

    return render(request, 'core/show_news.html', context=context)


def search(request):
    return render(request, 'core/search.html', context={})
