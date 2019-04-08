import json
from tests.models.tests import *
from core.additional import isfloat
from django.db.models import Q
from django.template.loader import render_to_string



def dump_questions(test):
    def find_effs(choice):
        reseff = {}
        for result in results:
            try:
                effect = TestsEffect.objects.get((Q(choice=choice)) & (Q(result=result)))
            except TestsEffect.DoesNotExist:
                continue
            else:
                reseff[result] = effect

        return reseff

    questions = TestsQuestion.objects.filter(test=test)
    results = TestsResult.objects.filter(test=test)
    data = [
            {'title':question.question_title,
            'one_option':question.one_option, # одновариантный опрос (True/False)
            'choices':{
                choice.id:{
                    'title':choice.choice_desc,
                    'effects':{
                    result.id:effect.value for result,
                    effect in find_effs(choice).items()
                    }
                } for choice in (TestsChoice.objects.filter(question=question))
            }
        } for question in questions
    ]

    questions_path = f'questions{test.id}.js'
    with open(questions_path, 'w') as questions_file:
        questions_file.write('questions = ')
        json.dump(data, questions_file, ensure_ascii=False)
    test.questions_js = questions_path
    test.save()


def dump_test(test, context):
    test_path = f'test{test.id}.js'
    page = render_to_string('tests/tests_js.html', context=context)
    with open(test_path, 'w') as test_file:
        test_file.write(page)
    test.test_js = test_path
    test.save()


def is_valid_res(results, user_results):
    if len(results) != len(user_results):
        return False
    else:
        for result in results:
            if str(result.id) not in user_results.keys():
                return False

        for res_val in user_results.values():
            if isfloat(res_val):
                if not 0.0 <= float(res_val) <= 100.0:
                    return False

        return True
