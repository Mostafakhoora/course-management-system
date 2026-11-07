from celery import shared_task
from django.core.mail import send_mail


@shared_task
def test_celery():
    return "Celery is working!"



@shared_task
def send_course_email(student_email, student_name, course_title):

    subject = 'ثبت نام در دوره با موفقیت انجام شد'

    message = f'''
سلام {student_name}

ثبت نام شما در دوره {course_title} با موفقیت انجام شد.

موفق باشید.
'''

    send_mail(
        subject,
        message,
        None,
        [student_email],
        fail_silently=False
    )

    return 'Email sent successfully'