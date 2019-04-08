from django.contrib import admin
import nested_admin
from .models.tests import *



class EffectInline(nested_admin.NestedTabularInline):
    fieldsets = [
        (None, {'fields': ['result', 'value']}),
    ]
    model = TestsEffect
    extra = 0


class ChoiceInline(nested_admin.NestedTabularInline):
    fieldsets = [
        (None, {'fields': ['choice_desc']}),
    ]
    inlines = [EffectInline]
    model = TestsChoice
    extra = 0


class QuestionInline(nested_admin.NestedStackedInline):
    fieldsets = [
        ('QUESTION', {'fields': ['question_title', 'one_option']}),
    ]
    inlines = [ChoiceInline]
    model = TestsQuestion
    extra = 0


class ResultInline(nested_admin.NestedTabularInline):
    fieldsets = [
        (None, {'fields': ['result_title', 'result_desc', 'result_image']}),
    ]
    model = TestsResult
    extra = 0


class TestAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        ('TEST', {'fields': ['pub_date', 'test_title', 'test_desc', 'brief', 'test_image', 'published']}),
    ]
    inlines = [ResultInline, QuestionInline]
    list_display = ('test_title', 'pub_date', 'published')
    list_filter = ['pub_date']
    search_fields = ['test_title', 'test_desc']


admin.site.register(TestsTest, TestAdmin)


'''admin.site.register(TestsTest)
admin.site.register(TestsQuestion)
admin.site.register(TestsResult)
admin.site.register(TestsChoice)
admin.site.register(TestsEffect)'''
