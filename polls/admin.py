from django.contrib import admin
from .models.polls import *


class ChoiceInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': ['choice_text']}),
    ]
    model = PollsChoice
    extra = 0


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('POLLS POLL', {'fields': ['pub_date', 'poll_title', 'brief', 'one_option', 'published']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['poll_title', 'brief']


admin.site.register(PollsPoll, PollAdmin)
