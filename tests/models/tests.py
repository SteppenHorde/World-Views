from django.db import models
from django.utils import timezone
from core.storages.ya_storage import YAStorage



class TestsTest(models.Model):
    test_title = models.CharField(verbose_name='Название', max_length=100)
    test_desc = models.CharField(verbose_name='Описание', max_length=2000)
    brief = models.CharField(verbose_name='Краткое описание', help_text='Показывается на карточке теста', max_length=500)
    test_image = models.ImageField(upload_to='tests/images', verbose_name='Картинка', storage=YAStorage())
    questions_js = models.FileField(upload_to='tests/js', verbose_name='js файл с вопросами', help_text='Вообще не трогать', null=True, storage=YAStorage())
    test_js = models.FileField(upload_to='tests/js', verbose_name='js файл с тестом', help_text='Изменять только в случае, если тесту нужен какой-то особый js файл', null=True, storage=YAStorage())
    pub_date = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то этот тест будет опубликован немедленно', default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def __str__(self):
        return f"{self.test_title} ({'опубликован' if self.published else 'не опубликован'})"


class TestsResult(models.Model):
    test = models.ForeignKey(TestsTest, on_delete=models.CASCADE)
    result_title = models.CharField(verbose_name='Результат', max_length=100)
    result_desc = models.CharField(verbose_name='Описание', max_length=2000)
    result_image = models.ImageField(upload_to='tests/images', verbose_name='Картинка', storage=YAStorage())

    def __str__(self):
        return f'[{self.test.test_title}] {self.result_title}'


class TestsQuestion(models.Model):
    test = models.ForeignKey(TestsTest, on_delete=models.CASCADE)
    question_title = models.CharField(verbose_name='Вопрос', max_length=500)
    one_option = models.BooleanField(verbose_name='Одновариантный вопрос', help_text='Если установлен, то пользователь сможет выбрать только один вариант ответа, а варианты будут радиокнопками', default=True)

    def __str__(self):
        return f"{self.question_title} ({'одновариантный' if self.one_option else 'многовариантный'})"


class TestsChoice(models.Model):
    question = models.ForeignKey(TestsQuestion, on_delete=models.CASCADE)
    result = models.ManyToManyField(TestsResult, through="TestsEffect")
    choice_desc = models.CharField(verbose_name='Вариант ответа', max_length=300)

    def __str__(self):
        return f"[{self.choice_desc}] для [{self.question}]"


class TestsEffect(models.Model):
    result = models.ForeignKey(TestsResult, on_delete=models.CASCADE, verbose_name='Для какого результата')
    choice = models.ForeignKey(TestsChoice, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Размер эффекта', default=0)

    def __str__(self):
        return f"[{'+' if self.value > 0 else ''}{str(self.value)}] для [{self.result}] в [{str(self.choice)}]"
