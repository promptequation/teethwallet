from common.models import Company
from django.conf import settings
from django.db import models
from appointment.models import Appointment, AppointmentFollowUp


class Notification(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   null=True, blank=True
                                   )
    created_for = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name="notification_created_for"
                                    )
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                null=True, blank=True
                                )
    notification_type = models.CharField(max_length=255, null=True, blank=True)
    notification_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    appointment = models.ForeignKey(Appointment,
                                    on_delete=models.CASCADE,
                                    null=True, blank=True
                                    )
    appointment_follow_up = models.ForeignKey(AppointmentFollowUp,
                                              on_delete=models.CASCADE,
                                              null=True, blank=True
                                              )

    def __str__(self) -> str:
        return str(f"Created by: {self.created_by}, Created for: {self.created_for}")

    class Meta:
        ordering = ["-id"]
