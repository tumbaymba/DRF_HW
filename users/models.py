from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from studing.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)
    city = models.CharField(max_length=35, verbose_name='Город', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    pay_method = models.CharField(max_length=20, choices=[('cash', 'наличные'), ('transfer', 'перевод на счет')],
                                  verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f'Платеж: {self.user}, сумма: {self.amount}'


class Сurrent_payment(models.Model):
    payment_link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", null=True, blank=True)
    payment_id = models.CharField(max_length=255, verbose_name='id сессии оплаты', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Текущая оплата курса'
        verbose_name_plural = 'Текущие оплаты курса'

    def __str__(self):
        return f'Платеж для: {self.owner}, за курс: {self.course}'