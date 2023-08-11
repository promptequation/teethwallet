from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from api.models.user_model import MultiLanguage


class Duration(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='duration_created_by',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='duration_updated_by',
        blank=True, null=True
    )

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name_plural = "Durations"


class Tooth(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='tooth_created_by', blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='tooth_updated_by', blank=True, null=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name_plural = "Teeth"


class Treatment(models.Model):
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='treatment_created_by', blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='treatment_updated_by', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Treatments"


class TreatmentLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name


class Diagnostic(models.Model):
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='diagnostic_created_by', blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='diagnostic_updated_by', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Diagnostics"


class DiagnosticLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='specialization_created_by', blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='specialization_updated_by', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Specializations"


class Qualification(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='qualification_created_by',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='qualification_updated_by',
        blank=True, null=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Qualifications"


class QualificationLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    qualification = models.ForeignKey(
        Qualification, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


class LookUpType(models.Model):
    code = models.CharField(_('Code'), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lookUptype_created_by',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lookUptype_updated_by',
        blank=True, null=True
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name_plural = "LookUpTypes"


class LookUp(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
    group = models.ForeignKey(
        LookUpType, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(_('Code'), max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='look_up_created_by',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='look_up_updated_by',
        blank=True, null=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "LookUps"


class Company(models.Model):
    code = models.CharField(_('Code'), max_length=255, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
    street = models.CharField(
        _('Street'), max_length=250, blank=True, null=True)
    street2 = models.CharField(
        _('Street 2'), max_length=250, blank=True, null=True)
    state = models.CharField(_('VAT'), max_length=150, blank=True, null=True)
    city = models.CharField(_('City'), max_length=150, blank=True, null=True)
    zipcode = models.CharField(_('Zip'), max_length=255, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_(
        "Is Active"), default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_created_by',
        blank=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_updated_by',
        blank=True, null=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Companies"


class CompanyLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=255, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
    street = models.CharField(
        _('Street'), max_length=250, blank=True, null=True)
    street2 = models.CharField(
        _('Street 2'), max_length=250, blank=True, null=True)
    state = models.CharField(_('VAT'), max_length=150, blank=True, null=True)
    city = models.CharField(_('City'), max_length=150, blank=True, null=True)
    zipcode = models.CharField(_('Zip'), max_length=255, blank=True, null=True)
    country = models.CharField(
        _('Country'), max_length=150, blank=True, null=True)

    def __str__(self):
        return self.company.name


class CompanyUser(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_user_doctor',
        null=True, blank=True
    )
    status = models.ForeignKey(
        LookUp,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    is_owner = models.BooleanField(verbose_name=_(
        "Is Owner"),
        default=False,
        null=True
    )
    joined_datetime = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now=True)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_user_requested_by',
        null=True, blank=True
    )
    approval_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_user_approval_by',
        null=True, blank=True
    )
    approval_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_(
        "Is Active"), default=True, null=True)

    # For Doctor
    DOCTOR_REQUEST = "DOCTOR_REQUEST"
    DOCTOR_APPROVAL = "DOCTOR_APPROVAL"

    # For Owner
    OWNER_REQUEST = "OWNER_REQUEST"
    OWNER_APPROVAL = "OWNER_APPROVAL"

    # For Doctor Patient Request
    PATIENT_REQUEST_DOCTOR = "PATIENT_REQUEST_DOCTOR"
    DOCTOR_ACCEPT_PATIENT_REQUEST = "DOCTOR_ACCEPT_PATIENT_REQUEST"

    # For Doctor Patient Accept
    DOCTOR_REQUEST_PATIENT = "DOCTOR_REQUEST_PATIENT"
    PATIENT_ACCEPT_DOCTOR_REQUEST = "PATIENT_ACCEPT_DOCTOR_REQUEST"

    # For Doctor Patient Revoke
    DOCTOR_REVOKE_PATIENT_ACCESS = "DOCTOR_REVOKE_PATIENT_ACCESS"
    PATIENT_REVOKE_DOCTOR_ACCESS = "PATIENT_REVOKE_DOCTOR_ACCESS"

    REQUEST_TYPE_CHOICES = [
        (DOCTOR_REQUEST, "DOCTOR_REQUEST"),
        (DOCTOR_APPROVAL, "DOCTOR_APPROVAL"),
        (OWNER_REQUEST, "OWNER_REQUEST"),
        (OWNER_APPROVAL, "OWNER_APPROVAL"),
        (PATIENT_REQUEST_DOCTOR, "PATIENT_REQUEST_DOCTOR"),
        (DOCTOR_REQUEST_PATIENT, "DOCTOR_REQUEST_PATIENT"),
        (DOCTOR_ACCEPT_PATIENT_REQUEST, "DOCTOR_ACCEPT_PATIENT_REQUEST"),
        (PATIENT_ACCEPT_DOCTOR_REQUEST, "PATIENT_ACCEPT_DOCTOR_REQUEST"),
        (DOCTOR_REVOKE_PATIENT_ACCESS, "DOCTOR_REVOKE_PATIENT_ACCESS"),
        (PATIENT_REVOKE_DOCTOR_ACCESS, "PATIENT_REVOKE_DOCTOR_ACCESS"),
    ]

    request_type = models.CharField(_('Request Type'), max_length=255,
                                    choices=REQUEST_TYPE_CHOICES,
                                    blank=True, null=True
                                    )

    class Meta:
        verbose_name_plural = "CompanyUsers"


class DoctorType(models.Model):
    type = models.CharField(_('Type'), max_length=255, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_type_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_type_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        verbose_name_plural = "DoctorTypes"


class Question(models.Model):
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    is_conditional_question = models.BooleanField(verbose_name=_(
        "Is Conditional Question"), default=False, null=True)
    element_type = models.ForeignKey(
        LookUp,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    serial_no = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Questions"


class QuestionResponse(models.Model):
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    serial_no = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_response_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_response_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "QuestionResponses"


class QuestionResponseLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    question_response = models.ForeignKey(
        QuestionResponse, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class Priority(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='priority_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='priority_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Priorities"


class PriorityLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class SpecializationLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class QuestionLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class AppointmentCode(models.Model):
    CodeTypes = [
        ('P', 'Problem'),
        ('D', 'Decision'),
        ('T', 'Treatment'),
        ('M', 'Material'),
    ]
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    code_type = models.CharField(
        max_length=1, choices=CodeTypes, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.code_type == 'P':
            self.name = 'P-' + self.code
        elif self.code_type == 'D':
            self.name = 'D-' + self.code
        elif self.code_type == 'T':
            self.name = 'T-' + self.code
        elif self.code_type == 'M':
            self.name = 'M-' + self.code
        super(AppointmentCode, self).save(*args, **kwargs)


class PredefinedAppointmentFollowUpCombination(models.Model):
    follow_up_date = models.DateTimeField(blank=True, null=True)
    diagnosis = models.ForeignKey(
        Diagnostic,
        on_delete=models.CASCADE,
        related_name='predefined_appointment_follow_up_diagnostic',
        null=True, blank=True
    )
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE,
        related_name='predefined_appointment_follow_up_treatment',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predefined_appointment_follow_up_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predefined_appointment_follow_up_updated_by",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"Diagnosis: {self.diagnosis}, Treatment: {self.treatment}")

    class Meta:
        verbose_name_plural = "PredefinedAppointmentFollowUpCombinations"
