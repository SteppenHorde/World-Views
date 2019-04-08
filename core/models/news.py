from django.db import models
from django.utils import timezone
from core.storages.ya_storage import YAStorage



class News(models.Model):
    news_title = models.CharField(verbose_name='Новость', max_length=100)
    news_text = models.CharField(verbose_name='Текст', max_length=10000)
    brief = models.CharField(verbose_name='Новость кратко', help_text='Показывается на карточке новости', max_length=700, default='')
    news_image = models.ImageField(upload_to='news/images', verbose_name='Картинка', storage=YAStorage())
    pub_date = models.DateTimeField(verbose_name='Дата новости', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то эта новость будет опубликована немедленно', default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def __str__(self):
        return f'{self.news_title} (опубликован)' if self.published else self.news_title
