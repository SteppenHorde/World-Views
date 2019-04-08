from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from polls.models.polls import *
from django.db.models import F

from collections import OrderedDict



def polls(request):
    polls_list = PollsPoll.objects.filter(published=True).order_by('-pub_date')
    polls = OrderedDict()
    completed_polls = set()
    selected_choices = request.session.get('selected_choices', list())
    for poll in polls_list:
        choices = PollsChoice.objects.filter(question=poll)
        if set(selected_choices) & set((choice.id for choice in choices)):
            completed_polls.add(poll.id)
        polls[poll] = choices

    context = {
        'polls':polls,
        'selected_choices':selected_choices,
        'completed_polls':completed_polls,
        }

    return render(request, 'polls/polls.html', context=context)


def polls_vote(request, poll_id):
    try:
        poll = PollsPoll.objects.get(
            Q(published=True) & Q(pk=poll_id)
            )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if not request.session.get('selected_choices', False): # если у пользователя ещё нет куки
        request.session['selected_choices'] = list() # инициализируем её ему
        request.session.set_expiry(63072000) # два года храним куку
    try:
        all_choices = PollsChoice.objects.filter(question=poll)
        selected_choices = set()
        for name in request.POST.keys():
            if name.startswith('choice'):
                selected_choices.add(all_choices.get(pk=request.POST.get(name)))

        if not len(request.POST.keys()) <= 1:
            poll.all_votes += 1
            poll.save()
        else:
            return
    except (KeyError, PollsChoice.DoesNotExist):
        return HttpResponse('Вы не сделали выбор!')
    else:
        for selected_choice in selected_choices:
            selected_choice.votes += 1
            selected_choice.save()
            request.session['selected_choices'].append(selected_choice.id)

        request.session.modified = True
        context = {
            'poll':poll,
            'choices':all_choices,
            'selected_choices':request.session['selected_choices'],
            }

        return render(request, 'polls/get_poll.html', context=context)
