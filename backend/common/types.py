from api.custom_node import CustomNode
from graphene_django import DjangoObjectType
from .filters import CompanyFilter, CompanyUserFilter, AppointmentCodeFilter
from .models import *
from api.models.user_model import MultiLanguage


class DurationType(DjangoObjectType):
    class Meta:
        model = Duration
        fields = "__all__"
        filter_fields = ['number']
        interfaces = (CustomNode,)


class ToothType(DjangoObjectType):
    class Meta:
        model = Tooth
        fields = "__all__"
        filter_fields = ['number']
        interfaces = (CustomNode,)


class DiagnosticType(DjangoObjectType):
    class Meta:
        model = Diagnostic
        fields = "__all__"
        filter_fields = ['name']
        interfaces = (CustomNode,)


class TreatmentType(DjangoObjectType):
    class Meta:
        model = Treatment
        fields = "__all__"
        filter_fields = ['name']
        interfaces = (CustomNode,)


class SpecializationType(DjangoObjectType):
    class Meta:
        model = Specialization
        fields = "__all__"
        filter_fields = ['name']
        interfaces = (CustomNode,)


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        fields = "__all__"
        filterset_class = CompanyFilter
        interfaces = (CustomNode,)


class CompanyUserType(DjangoObjectType):
    class Meta:
        model = CompanyUser
        fields = "__all__"
        filterset_class = CompanyUserFilter
        interfaces = (CustomNode,)


class LookUpTypeType(DjangoObjectType):
    class Meta:
        model = LookUpType
        fields = "__all__"
        interfaces = (CustomNode,)


class LookUpType(DjangoObjectType):
    class Meta:
        model = LookUp
        fields = "__all__"
        filter_fields = ['name']
        interfaces = (CustomNode,)


class PriorityType(DjangoObjectType):
    class Meta:
        model = Priority
        fields = "__all__"
        filter_fields = ['id', 'name', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"
        filter_fields = ['id', 'title', 'reference_id', 'element_type__id', 'is_conditional_question',
                         'serial_no', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class QuestionResponseType(DjangoObjectType):
    class Meta:
        model = QuestionResponse
        fields = "__all__"
        filter_fields = ['id', 'title', 'question__id', 'reference_id',
                         'serial_no', 'created_by__id', 'updated_by__id']
        interfaces = (CustomNode,)


class MultiLanguageType(DjangoObjectType):
    class Meta:
        model = MultiLanguage
        fields = "__all__"
        filter_fields = ["id", "name", "code"]
        interfaces = (CustomNode,)


class CompanyLangType(DjangoObjectType):
    class Meta:
        model = CompanyLang
        fields = "__all__"
        filter_fields = ["id", "lang__id", "lang__code", "company__id", "name"]
        interfaces = (CustomNode,)


class DiagnosticLangType(DjangoObjectType):
    class Meta:
        model = DiagnosticLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "diagnostic__id", "name"]
        interfaces = (CustomNode,)


class TreatmentLangType(DjangoObjectType):
    class Meta:
        model = TreatmentLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "treatment__id", "name"]
        interfaces = (CustomNode,)


class SpecializationLangType(DjangoObjectType):
    class Meta:
        model = SpecializationLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "specialization__id", "name"]
        interfaces = (CustomNode,)


class QuestionLangType(DjangoObjectType):
    class Meta:
        model = QuestionLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "question__id", "title"]
        interfaces = (CustomNode,)


class QuestionResponseLangType(DjangoObjectType):
    class Meta:
        model = QuestionResponseLang
        fields = "__all__"
        filter_fields = ["id", "lang__id", "lang__code",
                         "question_response__id", "title"]
        interfaces = (CustomNode,)


class QualificationLangType(DjangoObjectType):
    class Meta:
        model = QualificationLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "qualification__id", "name"]
        interfaces = (CustomNode,)


class PriorityLangType(DjangoObjectType):
    class Meta:
        model = PriorityLang
        fields = "__all__"
        filter_fields = ["id", "lang__id",
                         "lang__code", "priority__id", "name"]
        interfaces = (CustomNode,)


class AppointmentCodeType(DjangoObjectType):
    class Meta:
        model = AppointmentCode
        fields = "__all__"
        interfaces = (CustomNode,)
        filterset_class = AppointmentCodeFilter
