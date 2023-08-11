from celery import shared_task
from notification.models import Notification
from common.models import Company
from django.contrib.auth import get_user_model
User = get_user_model()


@shared_task(bind=True)
def appointment_reminder(self, created_by, created_for, company, notification_type, notification_text):
    Notification.objects.create(
        created_by=User.objects.get(pk=created_by),
        created_for=User.objects.get(pk=created_for),
        company=Company.objects.get(pk=company),
        notification_type=notification_type,
        notification_text=notification_text
    )
