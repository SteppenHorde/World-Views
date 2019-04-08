from django.db import models
from django.utils import timezone



class PollsPoll(models.Model):
    poll_title = models.CharField(verbose_name='Название опроса', max_length=100)
    brief = models.CharField(verbose_name='Кратко об опросе', help_text='Показывается на карточке опроса', max_length=700, default='')
    one_option = models.BooleanField(verbose_name='Одновариантный опрос', help_text='Если установлен, то пользователь сможет выбрать только один вариант ответа, а варианты будут радиокнопками', default=True)
    all_votes = models.IntegerField(verbose_name='Общее число голосов', default=0)
    pub_date = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то этот опрос будет опубликован немедленно', default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def __str__(self):
        return f"{self.poll_title} ({'опубликован' if self.published else 'не опубликован'})"


class PollsChoice(models.Model):
    question = models.ForeignKey(PollsPoll, on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name='Вариант ответа', max_length=200)
    votes = models.IntegerField(verbose_name='Число голосов', default=0)

    def __str__(self):
        return self.choice_text
