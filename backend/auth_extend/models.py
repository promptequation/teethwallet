from common.models import Specialization, Qualification
from django.conf import settings
from django.db import models


class UserSpecialization(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "UserSpecializations"


class UserQualification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "UserQualifications"
