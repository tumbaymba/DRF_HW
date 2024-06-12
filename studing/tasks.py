from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from studing.models import Course


@shared_task
def send_mail_about_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    subs = course.subscription_set.all()
    subs = subs.select_related('user')
    recipient_list = subs.values_list('user__email', flat=True)

    send_mail(
        subject=f'{course.title}',
        message=f'В {course.title} появились обновления',
        recipient_list=recipient_list,
        from_email=EMAIL_HOST_USER
    )
