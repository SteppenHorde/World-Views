from django.contrib import admin
from .models.news import *


class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pub_date', 'news_title', 'brief', 'news_text', 'news_image', 'published']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['news_title', 'news_text']


admin.site.register(News, NewsAdmin)
