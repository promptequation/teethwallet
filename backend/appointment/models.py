from common.models import *
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.models.user_model import MultiLanguage


class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_patient_id',
        null=True, blank=True
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_doctor_id',
        null=True, blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    start_date = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_updated_by",
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class AppointmentDetail(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='appointment_details',
        null=True, blank=True
    )
    tooth = models.ForeignKey(
        Tooth,
        on_delete=models.CASCADE,
        related_name='appointment_tooth',
        null=True, blank=True
    )
    diagnosis = models.ForeignKey(
        Diagnostic,
        on_delete=models.CASCADE,
        related_name='appointment_diagnostic',
        null=True, blank=True
    )
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE,
        related_name='appointment_treatment',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_details_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_details_updated_by",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"Patient: {self.appointment.patient}, Doctor: {self.appointment.doctor}")

    class Meta:
        verbose_name_plural = "AppointmentDetails"


class AppointmentFollowUp(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='appointment_follow_up',
        null=True, blank=True
    )
    follow_up_date = models.DateTimeField(blank=True, null=True)
    diagnosis = models.ForeignKey(
        Diagnostic,
        on_delete=models.CASCADE,
        related_name='appointment_follow_up_diagnostic',
        null=True, blank=True
    )
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE,
        related_name='appointment_follow_up_treatment',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_follow_up_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_follow_up_updated_by",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"Patient: {self.appointment.patient}, Doctor: {self.appointment.doctor}")

    class Meta:
        verbose_name_plural = "AppointmentFollowUps"


class AppointmentPriority(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_type_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_type_updated_by",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"Appointment ID: {self.appointment}")

    class Meta:
        verbose_name_plural = "AppointmentPriorities"


class AppointmentSpecialization(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_specialization_created_by",
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_specialization_updated_by",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"Appointment ID: {self.appointment}")

    class Meta:
        verbose_name_plural = "AppointmentSpecializations"


class AppointmentFile(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    file = models.FileField(
        upload_to='appointment/files/', null=True, blank=True)
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointmentFile_doctor',
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointmentFile_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointmentFile_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "AppointmentFiles"


class Survey(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='survey/files/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Surveys"


class SurveysQuestion(models.Model):
    parent_question = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='parent_title',
        null=True, blank=True
    )
    xml_question_id = models.IntegerField(blank=True, null=True)
    question_type = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.IntegerField(blank=True, null=True)
    is_conditional_question = models.BooleanField(blank=True, null=True)
    default_display = models.BooleanField(blank=True, null=True)
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_question_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_question_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "SurveysQuestions"


class SurveyQuestionResponse(models.Model):
    survey_question = models.ForeignKey(
        SurveysQuestion,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    xml_question_id = models.IntegerField(blank=True, null=True)
    xml_question_response_id = models.IntegerField(blank=True, null=True)
    question_response = models.CharField(
        _('Answer'), max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_question_response_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_question_response_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.question_response)

    class Meta:
        verbose_name_plural = "SurveyQuestionResponses"


class SurveyQuestionRelation(models.Model):
    survey_question = models.ForeignKey(
        SurveysQuestion,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="survey_question"
    )
    question_response = models.ForeignKey(
        SurveyQuestionResponse,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    xml_parent_question_id = models.IntegerField(blank=True, null=True)
    xml_question_response_id = models.IntegerField(blank=True, null=True)
    xml_question_response_target_question_id = models.IntegerField(
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AppointmentSurvey(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='appointment_survey',
        null=True, blank=True
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    is_finished = models.BooleanField(default=False, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_survey_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_survey_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.survey.name)

    class Meta:
        verbose_name_plural = "AppointmentSurveys"


class AppointmentSurveyQuestionResponse(models.Model):
    appointment_survey = models.ForeignKey(
        AppointmentSurvey,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    survey_question = models.ForeignKey(
        SurveysQuestion,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    question_response = models.ForeignKey(
        SurveyQuestionResponse,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    response_value = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_survey_question_response_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_survey_question_response_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.survey_question.title)

    class Meta:
        verbose_name_plural = "AppointmentSurveyQuestionResponses"


class Disease(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='disease_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='disease_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.question.id)

    class Meta:
        verbose_name_plural = "Diseases"


class DiseaseAnswer(models.Model):
    value = models.CharField(_('Value'), max_length=255, null=True, blank=True)
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    questionResponse = models.ForeignKey(
        QuestionResponse,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='disease_answer_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='disease_answer_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name_plural = "DiseaseAnswers"


class AppointmentLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.appointment)


class AppointmentShortCode(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, null=True, blank=True)
    appointment_code = models.ForeignKey(
        AppointmentCode, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_short_code_created_by',
        null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_short_code_updated_by',
        null=True, blank=True
    )

    def __str__(self):
        return str(self.appointment_code)

    class Meta:
        verbose_name_plural = "AppointmentShortCodes"
