import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from .models import *
from .types import *


class Query(graphene.ObjectType):
    appointments = DjangoFilterConnectionField(
        AppointmentType, patient=graphene.ID())

    @login_required
    def resolve_appointments(self, info, patient=None, doctor=None, is_active=None, **kwargs):
        if patient:
            if is_active is not None:
                return Appointment.objects.prefetch_related("appointment_survey").prefetch_related("appointment_follow_up").filter(patient__id=patient, is_active=is_active)
            return Appointment.objects.prefetch_related("appointment_survey").prefetch_related("appointment_follow_up").filter(patient__id=patient)
        if doctor:
            if is_active is not None:
                return Appointment.objects.prefetch_related("appointment_survey").prefetch_related("appointment_follow_up").filter(doctor__id=doctor, is_active=is_active)
            return Appointment.objects.prefetch_related("appointment_survey").prefetch_related("appointment_follow_up").filter(doctor__id=doctor)
        else:
            return Appointment.objects.prefetch_related("appointmentlang_set").prefetch_related("appointment_follow_up").all()

    appointmentDetails = graphene.List(AppointmentDetailType)

    @login_required
    def resolve_appointmentDetails(self, info, **kwargs):
        return AppointmentDetail.objects.all()

    appointmentPriorities = graphene.List(AppointmentProrityType)

    @login_required
    def resolve_appointmentPriorities(self, info, **kwargs):
        return AppointmentPriority.objects.all()

    appointmentSpecializations = graphene.List(AppointmentSpecializationType)

    @login_required
    def resolve_appointmentSpecializations(self, info, **kwargs):
        return AppointmentSpecialization.objects.all()

    appointmentFiles = graphene.List(AppointmentFileType)

    @login_required
    def resolve_appointmentFiles(self, info, **kwargs):
        return AppointmentFile.objects.all()

    surveys = graphene.List(SurveyType, pk=graphene.Int())

    @login_required
    def resolve_surveys(self, info, pk=None):
        if pk:
            return Survey.objects.prefetch_related("surveysquestion_set").filter(pk=pk)
        return Survey.objects.prefetch_related("surveysquestion_set").all()

    surveyQuestions = DjangoFilterConnectionField(SurveysQuestionType)

    @login_required
    def resolve_surveyQuestions(self, info, **kwargs):
        return SurveysQuestion.objects.prefetch_related("surveyquestionresponse_set").all()

    surveyQuestionResponses = DjangoFilterConnectionField(
        SurveyQuestionResponseType)

    @login_required
    def resolve_surveyQuestionResponses(self, info, **kwargs):
        return SurveyQuestionResponse.objects.prefetch_related("surveyquestionrelation_set").all()

    surveyQuestionRelations = DjangoFilterConnectionField(
        SurveyQuestionRelationType)

    @login_required
    def resolve_surveyQuestionRelations(self, info, **kwargs):
        return SurveyQuestionRelation.objects.all()

    appointmentSurveys = graphene.List(
        AppointmentSurveyType, appointment_id=graphene.Int())

    @login_required
    def resolve_appointmentSurveys(self, info, appointment_id=None):
        if appointment_id:
            return AppointmentSurvey.objects.filter(appointment=appointment_id)
        return AppointmentSurvey.objects.select_related("survey").prefetch_related("appointmentsurveyquestionresponse_set").all()

    appointmentSurveyQuestionResponse = DjangoFilterConnectionField(
        AppointmentSurveyQuestionResponseType)

    @login_required
    def resolve_appointmentSurveyQuestionResponses(self, info):
        return AppointmentSurveyQuestionResponse.objects.all()

    appointmentLang = DjangoFilterConnectionField(AppointmentLangType)

    @login_required
    def resolve_appointmentLang(self, info, **kwargs):
        return AppointmentLang.objects.all()

    appointmentshortCode = graphene.List(AppointmentShortCodeType)

    @login_required
    def resolve_appointmentshortCode(self, info, **kwargs):
        return AppointmentShortCode.objects.all()
