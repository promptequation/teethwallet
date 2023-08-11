from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from common.models import *
from appointment.models import *
from chat.models import Connection


@receiver(post_save, sender=CompanyUser)
def update_appointment_on_company_user_change(sender, instance, created, **kwargs):
    if not created:
        if instance.request_type == "DOCTOR_REVOKE_PATIENT_ACCESS" or instance.request_type == "PATIENT_REVOKE_DOCTOR_ACCESS":
            appointments = Appointment.objects.filter(
                doctor_id=instance.doctor.id, patient_id=instance.user.id)
            for appointment in appointments:
                appointment.is_active = False
                appointment.save()
            connections = Connection.objects.filter(
                sender=instance.user, receiver=instance.doctor) | Connection.objects.filter(
                    sender=instance.doctor, receiver=instance.user)
            for connection in connections:
                connection.is_active = False
                connection.save()
        if instance.request_type == "PATIENT_ACCEPT_DOCTOR_REQUEST" or instance.request_type == "DOCTOR_ACCEPT_PATIENT_REQUEST":
            appointments = Appointment.objects.filter(
                doctor_id=instance.doctor.id, patient_id=instance.user.id)
            for appointment in appointments:
                appointment.is_active = True
                appointment.save()
            connections = Connection.objects.filter(
                sender=instance.user, receiver=instance.doctor) | Connection.objects.filter(
                    sender=instance.doctor, receiver=instance.user)
            for connection in connections:
                connection.is_active = True
                connection.save()
        if instance.status.name == "Reject":
            appointments = Appointment.objects.filter(
                doctor_id=instance.doctor, patient_id=instance.user)
            for appointment in appointments:
                appointment.is_active = False
                appointment.save()
            connections = Connection.objects.filter(
                sender=instance.user, receiver=instance.doctor) | Connection.objects.filter(
                    sender=instance.doctor, receiver=instance.user)
            for connection in connections:
                connection.is_active = False
                connection.save()
        if instance.status.name == "Approve":
            appointments = Appointment.objects.filter(
                doctor_id=instance.doctor, patient_id=instance.user)
            for appointment in appointments:
                appointment.is_active = True
                appointment.save()
            connections = Connection.objects.filter(
                sender=instance.user, receiver=instance.doctor) | Connection.objects.filter(
                    sender=instance.doctor, receiver=instance.user)
            for connection in connections:
                connection.is_active = True
                connection.save()


@receiver(post_save, sender=AppointmentDetail)
def create_appointment_follow_up_on_appointment_change(sender, **kwargs):
    appointment_follow_ups = PredefinedAppointmentFollowUpCombination.objects.filter(
        diagnosis_id=kwargs["instance"].diagnosis.id, treatment_id=kwargs["instance"].treatment.id)
    for appointment_follow_up in appointment_follow_ups:
        time_difference = appointment_follow_up.follow_up_date - \
            appointment_follow_up.created_at
        appointment_follow_up_date = kwargs["instance"].appointment.start_date + time_difference
        try:
            appointment_follow_up_instance = AppointmentFollowUp.objects.get(
                appointment=kwargs["instance"].appointment,
                follow_up_date=appointment_follow_up_date,
                diagnosis=kwargs["instance"].diagnosis if kwargs["instance"].diagnosis else None,
                treatment=kwargs["instance"].treatment if kwargs["instance"].treatment else None,
            )
        except:
            appointment_follow_up_instance = AppointmentFollowUp.objects.create(
                appointment=kwargs["instance"].appointment,
                follow_up_date=appointment_follow_up_date,
                diagnosis=kwargs["instance"].diagnosis if kwargs["instance"].diagnosis else None,
                treatment=kwargs["instance"].treatment if kwargs["instance"].treatment else None,
            )


@receiver(post_save, sender=PredefinedAppointmentFollowUpCombination)
def create_appointment_follow_up_on_predefined_appointment_follow_up_change(sender, **kwargs):
    appointment_details = AppointmentDetail.objects.filter(
        diagnosis=kwargs["instance"].diagnosis, treatment=kwargs["instance"].treatment)
    appointments = [i.appointment for i in appointment_details]
    for appointment in appointments:
        time_difference = kwargs["instance"].follow_up_date - \
            kwargs["instance"].created_at
        appointment_follow_up_date = appointment.start_date + time_difference
        try:
            appointment_follow_up_instance = AppointmentFollowUp.objects.get(
                appointment=appointment,
                follow_up_date=appointment_follow_up_date,
                diagnosis=kwargs["instance"].diagnosis if kwargs["instance"].diagnosis else None,
                treatment=kwargs["instance"].treatment if kwargs["instance"].treatment else None,
            )
        except:
            appointment_follow_up_instance = AppointmentFollowUp.objects.create(
                appointment=appointment,
                follow_up_date=appointment_follow_up_date,
                diagnosis=kwargs["instance"].diagnosis if kwargs["instance"].diagnosis else None,
                treatment=kwargs["instance"].treatment if kwargs["instance"].treatment else None,
            )
