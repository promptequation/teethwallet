import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from api.models.user_model import MultiLanguage
from .models import *
from .types import *


class Query(graphene.ObjectType):
    durations = graphene.List(DurationType)

    @login_required
    def resolve_durations(self, info, **kwargs):
        return Duration.objects.all()

    teeth = graphene.List(ToothType)

    @login_required
    def resolve_teeth(self, info, **kwargs):
        return Tooth.objects.all()

    diagnostics = graphene.List(DiagnosticType)

    @login_required
    def resolve_diagnostics(self, info, **kwargs):
        return Diagnostic.objects.prefetch_related('diagnosticlang_set').all()

    treatments = graphene.List(TreatmentType)

    @login_required
    def resolve_treatments(self, info, **kwargs):
        return Treatment.objects.prefetch_related('treatmentlang_set').all()

    specializations = graphene.List(SpecializationType)

    @login_required
    def resolve_specializations(self, info, **kwargs):
        return Specialization.objects.prefetch_related('specializationlang_set').all()

    companies = DjangoFilterConnectionField(CompanyType)

    def resolve_companies(self, info, **kwargs):
        return Company.objects.prefetch_related('companylang_set').all()

    company = graphene.Field(CompanyType, company_id=graphene.Int())

    def resolve_company(self, info, company_id=None):
        if company_id:
            return Company.objects.get(pk=company_id)

    userCompany = DjangoFilterConnectionField(CompanyUserType)

    def resolve_userCompany(self, info, **kwargs):
        return CompanyUser.objects.all()

    approvalStatuses = graphene.List(LookUpType)
    approvalStatusFilters = DjangoFilterConnectionField(LookUpType)

    def resolve_approvalStatuses(self, info, **kwargs):
        return LookUp.objects.filter(group__code="APPROVAL")

    def resolve_approvalStatusFilters(self, info, **kwargs):
        return LookUp.objects.filter(group__code="APPROVAL")

    elementTypes = graphene.List(LookUpType)

    def resolve_elementTypes(self, info):
        return LookUp.objects.filter(group__code="ELEMENT_TYPE")

    priorities = graphene.List(PriorityType)

    def resolve_priorities(self, info, **kwargs):
        return Priority.objects.prefetch_related('prioritylang_set').all()

    questions = DjangoFilterConnectionField(QuestionType)

    def resolve_questions(self, info, **kwargs):
        return Question.objects.prefetch_related('questionlang_set').all()

    questionResponses = graphene.List(QuestionResponseType)

    def resolve_questionResponses(self, info, **kwargs):
        return QuestionResponse.objects.prefetch_related('questionresponseslang_set').all()

    multiLanguage = graphene.List(MultiLanguageType)

    def resolve_multiLanguage(self, info, **kwargs):
        return MultiLanguage.objects.all()

    companyLang = graphene.List(CompanyLangType)

    def resolve_companyLang(self, info, **kwargs):
        return CompanyLang.objects.all()

    diagnosticLang = graphene.List(DiagnosticLangType)

    def resolve_diagnosticLang(self, info, **kwargs):
        return DiagnosticLang.objects.all()

    treatmentLang = graphene.List(TreatmentLangType)

    def resolve_treatmentLang(self, info, **kwargs):
        return TreatmentLang.objects.all()

    specializationLang = graphene.List(SpecializationLangType)

    def resolve_specializationLang(self, info, **kwargs):
        return SpecializationLang.objects.all()

    questionLang = graphene.List(QuestionLangType)

    def resolve_questionLang(self, info, **kwargs):
        return QuestionLang.objects.all()

    questionResponseLang = graphene.List(QuestionResponseLangType)

    def resolve_questionResponseLang(self, info, **kwargs):
        return QuestionResponseLang.objects.all()

    qualificationLang = graphene.List(QualificationLangType)

    def resolve_qualificationLang(self, info, **kwargs):
        return QualificationLang.objects.all()

    priorityLang = graphene.List(PriorityLangType)

    def resolve_priorityLang(self, info, **kwargs):
        return PriorityLang.objects.all()

    appointmentCode = DjangoFilterConnectionField(AppointmentCodeType)

    @login_required
    def resolve_appointmentCode(self, info, **kwargs):
        return AppointmentCode.objects.all()
