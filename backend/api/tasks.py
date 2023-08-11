from backend.celery import app
from django.core.mail import send_mail


@app.task(bind=True)
def registration_send_email(self, user):
    send_mail(
        'Thanks for registering with Oral eHealth',
        'Here is the message.',
        'oral@oral.com',
        [user.email],
        fail_silently=False,
    )
