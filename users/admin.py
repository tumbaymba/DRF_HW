from django.contrib import admin
from users.models import User, Payment


admin.site.register(User)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'payment_date', 'paid_course', 'paid_lesson','amount','pay_method',)
    list_filter = ('payment_date', 'paid_course', 'paid_lesson',)