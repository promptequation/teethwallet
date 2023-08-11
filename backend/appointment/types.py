from api.custom_node import CustomNode
from graphene_django import DjangoObjectType
from .models import *


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment
        fields = "__all__"
        filter_fields = ['id', 'start_date', 'duration', 'note', 'patient__id', 'doctor__id', 'company__id',
                         'created_by__id', 'updated_by__id', 'is_deleted', "is_active"]
        interfaces = (CustomNode,)


class AppointmentFollowUpType(DjangoObjectType):
    class Meta:
        model = AppointmentFollowUp
        fields = "__all__"
        filter_fields = ['id', 'appointment__id', 'created_by__id',
                         'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentDetailType(DjangoObjectType):
    class Meta:
        model = AppointmentDetail
        fields = "__all__"
        filter_fields = ['id', 'appointment__id', 'tooth__id', 'diagnosis__id', 'treatment__id', 'created_by__id',
                         'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentProrityType(DjangoObjectType):
    class Meta:
        model = AppointmentPriority
        fields = "__all__"
        filter_fields = ['id', 'appointment__id',
                         'priority__id', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentSpecializationType(DjangoObjectType):
    class Meta:
        model = AppointmentSpecialization
        fields = "__all__"
        filter_fields = ['id', 'appointment__id',
                         'specialization__id', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentFileType(DjangoObjectType):
    class Meta:
        model = AppointmentFile
        fields = "__all__"
        filter_fields = ['id', 'name', 'appointment__id',
                         'doctor__id', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class DiseaseType(DjangoObjectType):
    class Meta:
        model = Disease
        fields = "__all__"
        filter_fields = ['id', 'question__id', 'user__id',
                         'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class DiseaseAnswerType(DjangoObjectType):
    class Meta:
        model = DiseaseAnswer
        fields = "__all__"
        filter_fields = ['id', 'value', 'disease__id',
                         'questionResponse__id', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class SurveyType(DjangoObjectType):
    class Meta:
        model = Survey
        fields = "__all__"
        filter_fields = ['id', 'name', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class SurveysQuestionType(DjangoObjectType):
    class Meta:
        model = SurveysQuestion
        fields = "__all__"
        filter_fields = ['id', 'parent_question_id', 'title',
                         'survey__id', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class SurveyQuestionResponseType(DjangoObjectType):
    class Meta:
        model = SurveyQuestionResponse
        fields = "__all__"
        filter_fields = ['survey_question__id', 'question_response',
                         'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class SurveyQuestionRelationType(DjangoObjectType):
    class Meta:
        model = SurveyQuestionRelation
        fields = "__all__"
        filter_fields = ['survey_question',
                         "question_response",
                         "xml_parent_question_id", "xml_question_response_id",
                         'xml_question_response_target_question_id',
                         ]
        interfaces = (CustomNode,)


class AppointmentSurveyType(DjangoObjectType):
    class Meta:
        model = AppointmentSurvey
        fields = "__all__"
        filter_fields = ['id', 'appointment__id', 'survey__id',
                         'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentSurveyQuestionResponseType(DjangoObjectType):
    class Meta:
        model = AppointmentSurveyQuestionResponse
        fields = "__all__"
        filter_fields = ['appointment_survey', 'appointment_survey__id', 'survey_question__id', 'question_response__id', 'created_by__id',
                         'updated_by__id']
        interfaces = (CustomNode,)


class AppointmentLangType(DjangoObjectType):
    class Meta:
        model = AppointmentLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "appointment__id", "note"]
        interfaces = (CustomNode,)


class AppointmentShortCodeType(DjangoObjectType):
    class Meta:
        model = AppointmentShortCode
        fields = "__all__"
        filter_fields = ["id", "appointment_code__id",
                         "appointment__id", "created_by__id", "updated_by__id"]
        interfaces = (CustomNode,)
