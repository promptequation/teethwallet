from pprint import pprint
from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
from appointment.models import Appointment, AppointmentFollowUp
from common.models import CompanyUser
from django.core.exceptions import ValidationError
from django.db.models.signals import *
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=CompanyUser)
def create_notification_on_company_user_change(sender, **kwargs):
    if kwargs["instance"]:
        if kwargs["instance"].request_type == "DOCTOR_REQUEST":
            Notification.objects.create(
                created_by=kwargs["instance"].user,
                created_for=kwargs["instance"].company.created_by,
                company=kwargs["instance"].company,
                notification_type=kwargs["instance"].request_type,
                notification_text="Request to Join Your Company"
            )
        elif kwargs["instance"].request_type == "DOCTOR_APPROVAL":
            Notification.objects.create(
                created_by=kwargs["instance"].user,
                created_for=kwargs["instance"].company.created_by,
                company=kwargs["instance"].company,
                notification_type=kwargs["instance"].request_type,
                notification_text="Accept You in Company"
            )
        elif kwargs["instance"].request_type == "OWNER_REQUEST":
            Notification.objects.create(
                created_by=kwargs["instance"].company.created_by,
                created_for=kwargs["instance"].user,
                company=kwargs["instance"].company,
                notification_type=kwargs["instance"].request_type,
                notification_text="Request to Join The Company"
            )
        elif kwargs["instance"].request_type == "OWNER_APPROVAL":
            Notification.objects.create(
                created_by=kwargs["instance"].company.created_by,
                created_for=kwargs["instance"].user,
                company=kwargs["instance"].company,
                notification_type=kwargs["instance"].request_type,
                notification_text="Accept your Join Request in Company"
            )
        elif kwargs["instance"].request_type == "PATIENT_REQUEST_DOCTOR":
            Notification.objects.create(
                created_by=kwargs["instance"].requested_by,
                created_for=kwargs["instance"].doctor,
                notification_type=kwargs["instance"].request_type,
                notification_text="Request to Give Access as a Doctor"
            )
        elif kwargs["instance"].request_type == "DOCTOR_ACCEPT_PATIENT_REQUEST":
            Notification.objects.create(
                created_by=kwargs["instance"].doctor,
                created_for=kwargs["instance"].user,
                notification_type=kwargs["instance"].request_type,
                notification_text="Give access as a Doctor"
            )
        elif kwargs["instance"].request_type == "DOCTOR_REQUEST_PATIENT":
            Notification.objects.create(
                created_by=kwargs["instance"].doctor,
                created_for=kwargs["instance"].user,
                notification_type=kwargs["instance"].request_type,
                notification_text="Request to Have Access as a Patient"
            )
        elif kwargs["instance"].request_type == "PATIENT_ACCEPT_DOCTOR_REQUEST":
            Notification.objects.create(
                created_by=kwargs["instance"].user,
                created_for=kwargs["instance"].doctor,
                notification_type=kwargs["instance"].request_type,
                notification_text="Give access as a Patient"
            )
        elif kwargs["instance"].request_type == "DOCTOR_REVOKE_PATIENT_ACCESS":
            Notification.objects.create(
                created_by=kwargs["instance"].doctor,
                created_for=kwargs["instance"].user,
                notification_type=kwargs["instance"].request_type,
                notification_text="Revoke access as a Doctor"
            )
        elif kwargs["instance"].request_type == "PATIENT_REVOKE_DOCTOR_ACCESS":
            Notification.objects.create(
                created_by=kwargs["instance"].user,
                created_for=kwargs["instance"].doctor,
                notification_type=kwargs["instance"].request_type,
                notification_text="Revoke access as a Patient"
            )
        else:
            pass
    else:
        raise ValidationError("Please fill the form correctly.")


@receiver(post_save, sender=Notification)
def all_notification(sender, **kwargs):
    if kwargs["created"]:
        company_name = kwargs["instance"].company
        notification_receiver = kwargs["instance"].created_for.id
        company_name = kwargs["instance"].company
        if company_name is not None:
            company_name = kwargs["instance"].company.name
        else:
            company_name = "None"
        appointment = None
        appointment_follow_up = None
        try:
            if Appointment.objects.filter(
                    pk=kwargs["instance"].appointment.id).first():
                appointment = Appointment.objects.filter(
                    pk=kwargs["instance"].appointment.id).first().id

            if AppointmentFollowUp.objects.filter(
                    appointment_id=kwargs["instance"].appointment.id).last():
                appointment_follow_up = AppointmentFollowUp.objects.filter(
                    appointment_id=kwargs["instance"].appointment.id).last().follow_up_date
        except:
            pass
        notify = {
            'data': {'notifications': [{'id': str(kwargs["instance"].id),
                                        'appointment': {'id': str(appointment)},
                                        "appointmentFollowUp": {'followUpDate': str(appointment_follow_up)},
                                        'createdBy': {'name': kwargs["instance"].created_by.name},
                                        'createdFor': {'name': kwargs["instance"].created_for.name},
                                        'company': {'name': company_name},
                                        'notificationText': kwargs["instance"].notification_text,
                                        'notificationType': kwargs["instance"].notification_type,
                                        'createdAt': kwargs["instance"].created_at.isoformat(),
                                        'isRead': kwargs["instance"].is_read}]}
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notification_{notification_receiver}',
            {
                "type": "notify",
                "text": notify,
            },
        )


@receiver(post_save, sender=Appointment)
def create_notification_on_appointment_change(sender, **kwargs):
    if kwargs["instance"] and kwargs["created"]:
        notification = Notification.objects.create(
            created_by=kwargs["instance"].doctor,
            created_for=kwargs["instance"].patient,
            company=kwargs["instance"].company,
            notification_type="APPOINTMENT_CREATED",
            notification_text="Appointment Created",
            appointment=Appointment.objects.get(id=kwargs["instance"].id)
        )
        previous_day = kwargs["instance"].start_date - timedelta(days=1)
        previous_day_schedule, previous_day_created = CrontabSchedule.objects.get_or_create(
            minute=previous_day.time().minute,
            hour=previous_day.time().hour,
            day_of_month=previous_day.date().day,
            month_of_year=previous_day.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} Previous Day Appointment Reminder {previous_day}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_day_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )
        previous_hour = kwargs["instance"].start_date - timedelta(hours=1)
        previous_hour_schedule, previous_hour_created = CrontabSchedule.objects.get_or_create(
            minute=previous_hour.time().minute,
            hour=previous_hour.time().hour,
            day_of_month=previous_hour.date().day,
            month_of_year=previous_hour.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} previous Hour Appointment Reminder {previous_hour}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_hour_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )


@receiver(post_save, sender=Notification)
def send_message_on_notification(sender, **kwargs):
    if kwargs["instance"]:
        appointment = None
        try:
            appointment = Appointment.objects.get(
                id=kwargs["instance"].appointment.id)
        except:
            appointment = None
        try:
            appointment_follow_up = AppointmentFollowUp.objects.filter(
                appointment=Appointment.objects.get(
                    id=kwargs["instance"].appointment.id)).first()
        except:
            appointment_follow_up = None
        try:
            device = FCMDevice.objects.filter(user=User.objects.get(
                pk=kwargs["instance"].created_for.id)).first()
            message = Message(
                token=device.registration_id,
                data={
                    "id": str(kwargs["instance"].id),
                    "isRead": str(kwargs["instance"].is_read),
                    "createdBy": str(kwargs["instance"].created_by.name),
                    "createdFor": str(kwargs["instance"].created_for.name),
                    "notificationText": str(kwargs["instance"].notification_text),
                    "notificationType": str(kwargs["instance"].notification_type),
                    "appointment": str(appointment),  # id
                    # date
                    "appointment_follow_up": str(appointment_follow_up),
                }
            )
            response = device.send_message(message)
        except:
            pass


@receiver(post_save, sender=AppointmentFollowUp)
def create_notification_for_patient_on_appointment_follow_up_create(sender, **kwargs):
    if kwargs["instance"] and kwargs["created"]:
        notification = Notification.objects.create(
            created_by=kwargs["instance"].appointment.doctor,
            created_for=kwargs["instance"].appointment.patient,
            company=kwargs["instance"].appointment.company,
            notification_type="APPOINTMENT_FOLLOW_UP_CREATED",
            notification_text="Appointment Follow Up Created",
            appointment=Appointment.objects.get(
                id=kwargs["instance"].appointment.id),
            appointment_follow_up=AppointmentFollowUp.objects.get(
                id=kwargs["instance"].id
            )
        )
        previous_day = kwargs["instance"].follow_up_date - timedelta(days=1)
        previous_day_schedule, previous_day_created = CrontabSchedule.objects.get_or_create(
            minute=previous_day.time().minute,
            hour=previous_day.time().hour,
            day_of_month=previous_day.date().day,
            month_of_year=previous_day.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} Previous Day Appointment FollowUp Reminder For Patient {previous_day}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_day_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )
        previous_hour = kwargs["instance"].follow_up_date - timedelta(hours=1)
        previous_hour_schedule, previous_hour_created = CrontabSchedule.objects.get_or_create(
            minute=previous_hour.time().minute,
            hour=previous_hour.time().hour,
            day_of_month=previous_hour.date().day,
            month_of_year=previous_hour.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} previous Hour Appointment FollowUp Reminder For Patient {previous_hour}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_hour_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )


@receiver(post_save, sender=AppointmentFollowUp)
def create_notification_for_doctor_on_appointment_follow_up_create(sender, **kwargs):
    if kwargs["instance"] and kwargs["created"]:
        notification = Notification.objects.create(
            created_by=kwargs["instance"].appointment.patient,
            created_for=kwargs["instance"].appointment.doctor,
            company=kwargs["instance"].appointment.company,
            notification_type="APPOINTMENT_FOLLOW_UP_CREATED",
            notification_text="Appointment Follow Up Created",
            appointment=Appointment.objects.get(
                id=kwargs["instance"].appointment.id),
            appointment_follow_up=AppointmentFollowUp.objects.get(
                id=kwargs["instance"].id
            )
        )
        previous_day = kwargs["instance"].follow_up_date - timedelta(days=1)
        previous_day_schedule, previous_day_created = CrontabSchedule.objects.get_or_create(
            minute=previous_day.time().minute,
            hour=previous_day.time().hour,
            day_of_month=previous_day.date().day,
            month_of_year=previous_day.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} Previous Day Appointment FollowUp Reminder For Doctor {previous_day}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_day_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )
        previous_hour = kwargs["instance"].follow_up_date - timedelta(hours=1)
        previous_hour_schedule, previous_hour_created = CrontabSchedule.objects.get_or_create(
            minute=previous_hour.time().minute,
            hour=previous_hour.time().hour,
            day_of_month=previous_hour.date().day,
            month_of_year=previous_hour.date().month,
        )
        PeriodicTask.objects.get_or_create(
            name=f"{kwargs['instance'].id} previous Hour Appointment FollowUp Reminder For Doctor {previous_hour}",
            task="appointment.tasks.appointment_reminder",
            crontab=previous_hour_schedule,
            one_off=True,
            start_time=kwargs['instance'].created_at,
            args=json.dumps([notification.created_by.id, notification.created_for.id, notification.company.id,
                            notification.notification_type, notification.notification_text]),
        )
