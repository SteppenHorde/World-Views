from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.template import loader
from tests.models.tests import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from os.path import isfile
from tests.additional import dump_test, dump_questions, is_valid_res
from collections import OrderedDict



def tests(request):
    tests = TestsTest.objects.filter(published=True).order_by('-pub_date')
    context = {
        'tests': tests,
        }
    return render(request, 'tests/tests.html', context=context)


def show_test(request, test_id):
    try:
        test = TestsTest.objects.get(
            Q(published=True) & Q(pk=test_id)
            )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    context = {
        'test': test,
        }
    return render(request, 'tests/show_test.html', context=context)


def quiz_test(request, test_id):
    try:
        test = TestsTest.objects.get(
            Q(published=True) & Q(pk=test_id)
            )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    context = {
        'test': test,
        }

    if bool(test.test_js.name) == False:
        results = TestsResult.objects.filter(test=test)
        context['results'] = results
        dump_test(test, context)

    if bool(test.questions_js.name) == False:
        dump_questions(test)

    return render(request, 'tests/quiz_test.html', context=context)


@require_GET
def tests_results(request, test_id):
    try:
        test = TestsTest.objects.get(
            Q(published=True) & Q(pk=test_id)
            )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    all_results = TestsResult.objects.filter(test=test)
    user_results_QD = request.GET
    if not is_valid_res(all_results, user_results_QD):
        return HttpResponse('Введённые параметры не валидны')
    else:
        user_results = {}
        for result_id, result_val in user_results_QD.items():
            user_results[int(result_id)] = float(result_val)

        user_results_ordered = []
        for k in sorted(user_results, key=(lambda k: user_results[k]), reverse=True):
            user_results_ordered.append((user_results[k], all_results.get(pk=k)))

        context = {
            'test':test,
            'results':user_results_ordered,
         }

        return render(request, 'tests/tests_results.html', context=context)
