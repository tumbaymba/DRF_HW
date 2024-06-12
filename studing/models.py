from django.db import models
from django.conf import settings


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью курса', null=True, blank=True)
    description = models.TextField(verbose_name='Описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Владелец')
    price = models.PositiveIntegerField(default=10000, verbose_name='стоимость курса')

    def str(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название урока', unique=True)
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью урока', null=True, blank=True)
    description = models.TextField(verbose_name='Описание урока')
    video_url = models.URLField(verbose_name='Ссылка на видео', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Владелец')

    def str(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='подписчик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'Подписан пользователь {self.user} на курс {self.course}'

    class Meta:
        verbose_name = 'подписка на обновление'
        verbose_name_plural = 'подписки на обновления'

