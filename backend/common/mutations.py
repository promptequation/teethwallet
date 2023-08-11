import graphene
from api.models.user_model import User
from common.handle_error import get_object_or_None
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from .models import *
from .types import *
from api.models.user_model import MultiLanguage


class DurationInput(graphene.InputObjectType):
    number = graphene.Int()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class DurationCreate(graphene.Mutation):
    class Arguments:
        input = DurationInput()

    durations = graphene.Field(DurationType)

    @staticmethod
    def mutate(root, info, input=None):
        duration = Duration.objects.filter(number=input.number).first()
        if duration:
            return DurationCreate(durations=duration)
        else:
            durations_instance = Duration(
                number=input.number,
                created_by_id=input.created_by,
                updated_by_id=input.updated_by or input.created_by,
            )
            durations_instance.save()
            return DurationCreate(durations=durations_instance)


class ToothInput(graphene.InputObjectType):
    number = graphene.Int()
    created_by = graphene.Int()
    updated_by = graphene.Int()


class CreateTooth(graphene.Mutation):
    class Arguments:
        input = ToothInput()

    tooth = graphene.Field(ToothType)

    @staticmethod
    def mutate(root, info, input=None):
        tooth = Tooth.objects.filter(number=input.number).first()
        if tooth:
            return CreateTooth(tooth=tooth)
        else:
            tooth_instance = Tooth(
                number=input.number,
                created_by_id=input.created_by,
                updated_by_id=input.updated_by or input.created_by,
            )
            tooth_instance.save()
            return CreateTooth(tooth=tooth_instance)


class DiagnosticInput(graphene.InputObjectType):
    name = graphene.String()
    lang = graphene.ID()
    created_by = graphene.Int()
    updated_by = graphene.Int()


class CreateDiagnostic(graphene.Mutation):
    class Arguments:
        input = DiagnosticInput()
    diagnostic = graphene.Field(DiagnosticType)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            diagonostic_lang = DiagnosticLang.objects.filter(
                name=input.name).first()
            diagonostic_id = diagonostic_lang.diagnostic.id
            diagnostic = Diagnostic.objects.get(pk=diagonostic_id)
            return CreateDiagnostic(diagnostic=diagnostic)
        except:
            diagnostic_instance = Diagnostic(
                created_by_id=input.created_by,
                updated_by_id=input.updated_by or input.created_by,
            )
            diagnostic_instance.save()
            diagnostic_lang = DiagnosticLang(
                diagnostic_id=diagnostic_instance.id,
                lang_id=input.lang,
                name=input.name,
            )
            diagnostic_lang.save()
            return CreateDiagnostic(diagnostic=diagnostic_instance)


class TreatmentInput(graphene.InputObjectType):
    name = graphene.String()
    lang = graphene.ID()
    created_by = graphene.Int()
    updated_by = graphene.Int()


class CreateTreatment(graphene.Mutation):
    class Arguments:
        input = TreatmentInput()

    treatment = graphene.Field(TreatmentType)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            treatment_lang = TreatmentLang.objects.filter(
                name=input.name).first()
            treatment_id = treatment_lang.treatment.id
            treatment = Treatment.objects.get(pk=treatment_id)
            return CreateTreatment(treatment=treatment)
        except:
            treatment_instance = Treatment(
                created_by_id=input.created_by,
                updated_by_id=input.updated_by or input.created_by,
            )
            treatment_instance.save()
            treatment_lang = TreatmentLang(
                treatment_id=treatment_instance.id,
                lang_id=input.lang,
                name=input.name,
            )
            treatment_lang.save()
            return CreateTreatment(treatment=treatment_instance)


class SpecializationInput(graphene.InputObjectType):
    name = graphene.String()
    created_by = graphene.Int()
    updated_by = graphene.Int()


class CreateSpecialization(graphene.Mutation):
    class Arguments:
        input = SpecializationInput()

    specialization = graphene.Field(SpecializationType)

    @staticmethod
    def mutate(root, info, input=None):
        specialization = Specialization.objects.filter(name=input.name).first()
        if specialization:
            return CreateSpecialization(specialization=specialization)
        else:
            specialization_instance = Specialization(
                name=input.name,
                created_by=input.created_by,
                updated_by=input.updated_by or input.created_by,
            )
            specialization_instance.save()
            return CreateSpecialization(specialization=specialization_instance)


class DeleteSpecialization(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    specialization = graphene.Field(SpecializationType)

    @staticmethod
    def mutate(root, info, id):
        specialization_instance = get_object_or_404(Specialization, pk=id)
        specialization_instance.delete()
        return None


class CompanyInput(graphene.InputObjectType):
    name = graphene.String()
    street = graphene.String()
    street2 = graphene.String()
    state = graphene.String()
    city = graphene.String()
    zipcode = graphene.String()
    country = graphene.String()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateCompany(graphene.Mutation):
    class Arguments:
        input = CompanyInput()

    company = graphene.Field(CompanyType)

    @staticmethod
    def mutate(root, info, input=None):
        created_by = User.objects.get(pk=input.created_by)
        updated_by = User.objects.get(pk=input.updated_by)
        comapny_instance = Company(
            name=input.name,
            street=input.street,
            street2=input.street2,
            state=input.state,
            city=input.city,
            zipcode=input.zipcode,
            country=input.country,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        comapny_instance.save()
        return CreateCompany(company=comapny_instance)


class UpdateCompanyInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    code = graphene.String()
    street = graphene.String()
    street2 = graphene.String()
    state = graphene.String()
    city = graphene.String()
    zipcode = graphene.String()
    country = graphene.String()
    is_active = graphene.Boolean()
    updated_by = graphene.ID()


class UpdateCompany(graphene.Mutation):
    class Arguments:
        input = UpdateCompanyInput()

    updateCompany = graphene.Field(CompanyType)

    @staticmethod
    def mutate(root, info, input=None):
        updated_by = get_object_or_404(User, pk=input.updated_by)
        update_company_instance = Company.objects.get(pk=input.id)
        if update_company_instance:
            update_company_instance.name = input.name
            update_company_instance.code = input.code
            update_company_instance.street = input.street
            update_company_instance.street2 = input.street2
            update_company_instance.state = input.state
            update_company_instance.city = input.city
            update_company_instance.zipcode = input.zipcode
            update_company_instance.country = input.country
            update_company_instance.is_active = input.is_active
            update_company_instance.updated_by = updated_by
            update_company_instance.save()
            return UpdateCompany(updateCompany=update_company_instance)
        return UpdateCompany(updateCompany=None)


class CompanyUserInput(graphene.InputObjectType):
    company = graphene.ID()
    user = graphene.ID()
    doctor = graphene.ID()
    group = graphene.ID()
    approval_by = graphene.ID()
    requested_by = graphene.ID()
    status = graphene.String()
    joined_datetime = graphene.DateTime()
    approval_at = graphene.DateTime()
    is_owner = graphene.Boolean()
    is_active = graphene.Boolean()
    request_type = graphene.String()


class CreateCompanyUser(graphene.Mutation):
    class Arguments:
        input = CompanyUserInput()

    companyUser = graphene.Field(CompanyUserType)

    @staticmethod
    def mutate(root, info, input=None):
        user = User.objects.get(id=input.user)
        doctor = get_object_or_None(User, id=input.doctor)
        group = get_object_or_None(Group, id=input.group)
        approval_by = get_object_or_None(User, id=input.approval_by)
        requested_by = get_object_or_None(User, id=input.requested_by)
        company = get_object_or_None(Company, id=input.company)
        approvalStatus = LookUp.objects.filter(name=input.status)
        status = None
        for status in approvalStatus:
            if input.status == status.name:
                status
        comapnyUser_instance = CompanyUser(
            company=company,
            user=user,
            doctor=doctor,
            group=group,
            approval_by=approval_by,
            requested_by=requested_by,
            status=status,
            joined_datetime=input.joined_datetime,
            approval_at=input.approval_at,
            is_owner=input.is_owner,
            is_active=input.is_active,
            request_type=input.request_type,
        )
        comapnyUser_instance.save()
        return CreateCompanyUser(companyUser=comapnyUser_instance)


class UpdateCompanyUserInput(graphene.InputObjectType):
    id = graphene.ID()
    company = graphene.ID()
    user = graphene.ID()
    doctor = graphene.ID()
    group = graphene.ID()
    approval_by = graphene.ID()
    requested_by = graphene.ID()
    status = graphene.String()
    joined_datetime = graphene.DateTime()
    approval_at = graphene.DateTime()
    is_owner = graphene.Boolean()
    is_active = graphene.Boolean()
    request_type = graphene.String()


class UpdateCompanyUser(graphene.Mutation):
    class Arguments:
        input = UpdateCompanyUserInput()

    companyuser_update = graphene.Field(CompanyUserType)

    @staticmethod
    def mutate(root, info, input=None):
        companyuser = CompanyUser.objects.filter(id=input.id)
        input_user = None
        input_doctor = None
        input_group = None
        input_approval_by = None
        input_requested_by = None
        input_company = None
        input_joined_datetime = None
        input_approval_at = None
        has_doctor = None
        has_group = None
        has_company = None
        has_approval_by = None
        has_requested_by = None
        input_request_type = None
        for i in companyuser:
            user = i.user.id
            if i.doctor:
                has_doctor = i.doctor.id
            else:
                none_doctor = None
            if i.group:
                has_group = i.group.id
            else:
                none_group = None
            if i.approval_by:
                has_approval_by = i.approval_by.id
            else:
                none_approval_by = None
            if i.requested_by:
                has_requested_by = i.requested_by.id
            else:
                none_requested_by = None
            if i.company:
                has_company = i.company.id
            else:
                none_company = None
        if input.user:
            input_user = get_object_or_None(User, id=input.user)
        else:
            exist_user = User.objects.get(id=user)
        if input.doctor:
            input_doctor = get_object_or_None(User, id=input.doctor)
        else:
            exist_doctor = get_object_or_None(User, id=has_doctor)
        if input.group:
            input_group = get_object_or_None(Group, id=input.group)
        else:
            exist_group = get_object_or_None(Group, id=has_group)
        if input.approval_by:
            input_approval_by = get_object_or_None(User, id=input.approval_by)
        else:
            exist_approval_by = get_object_or_None(User, id=has_approval_by)
        if input.requested_by:
            input_requested_by = get_object_or_None(
                User, id=input.requested_by)
        else:
            exist_requested_by = get_object_or_None(User, id=has_requested_by)
        if input.company:
            input_company = get_object_or_None(Company, id=input.company)
        else:
            exist_company = get_object_or_None(Company, id=has_company)
        bolean_instance = get_object_or_None(CompanyUser, id=input.id)
        status = None
        if input.status:
            approvalStatus = LookUp.objects.filter(name=input.status)
            for status in approvalStatus:
                if input.status == status.name:
                    status
        else:
            exist_status = get_object_or_None(CompanyUser, id=input.id)
        if input.joined_datetime:
            input_joined_datetime = input.joined_datetime
        else:
            exist_joined_datetime = get_object_or_None(
                CompanyUser, id=input.id)
        if input.approval_at:
            input_approval_at = input.approval_at
        else:
            exist_approval_at = get_object_or_None(CompanyUser, id=input.id)
        if input.request_type:
            input_request_type = input.request_type
        else:
            none_request_type = None
        companyuser_update_instance = CompanyUser.objects.get(pk=input.id)
        if companyuser_update_instance:
            companyuser_update_instance.user = input_user or exist_user
            companyuser_update_instance.doctor = input_doctor or exist_doctor
            companyuser_update_instance.group = input_group or exist_group
            companyuser_update_instance.approval_by = input_approval_by or exist_approval_by
            companyuser_update_instance.requested_by = input_requested_by or exist_requested_by
            companyuser_update_instance.company = input_company or exist_company
            companyuser_update_instance.status = status or exist_status.status
            companyuser_update_instance.joined_datetime = input_joined_datetime or exist_joined_datetime.joined_datetime
            companyuser_update_instance.approval_at = input_approval_at or exist_approval_at.approval_at
            companyuser_update_instance.request_type = input_request_type or input.request_type
            if input.is_owner == False:
                companyuser_update_instance.is_owner = False
            elif input.is_owner == True:
                companyuser_update_instance.is_owner = True
            else:
                companyuser_update_instance.is_owner = bolean_instance.is_owner
            if input.is_active == False:
                companyuser_update_instance.is_active = False
            elif input.is_active == True:
                companyuser_update_instance.is_active = True
            else:
                companyuser_update_instance.is_active = bolean_instance.is_active
            companyuser_update_instance.save()
            return UpdateCompanyUser(companyuser_update=companyuser_update_instance)
        return UpdateCompanyUser(companyuser_update=None)


class DeleteCompanyUser(graphene.Mutation):
    class Arguments:
        input = graphene.ID()

    companyuser = graphene.Field(CompanyUserType)

    @staticmethod
    def mutate(root, info, input):
        companyuser_instance = get_object_or_404(CompanyUser, pk=input)
        companyuser_instance.delete()
        return None


class QuestionInput(graphene.InputObjectType):
    title = graphene.String()
    reference_id = graphene.Int()
    serial_no = graphene.Int()
    element_type = graphene.String()
    is_conditional_question = graphene.Boolean()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateQuestion(graphene.Mutation):
    class Arguments:
        input = QuestionInput()

    questions = graphene.Field(QuestionType)

    @staticmethod
    def mutate(root, info, input=None):
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        elementTypes = LookUp.objects.filter(name=input.element_type)
        element = None
        for element in elementTypes:
            if input.element_type == element.name:
                element
        questions_instance = Question(
            title=input.title,
            reference_id=input.reference_id,
            serial_no=input.serial_no,
            element_type=element,
            is_conditional_question=input.is_conditional_question,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        questions_instance.save()
        return CreateQuestion(questions=questions_instance)


class QuestionResponseInput(graphene.InputObjectType):
    title = graphene.String()
    reference_id = graphene.Int()
    serial_no = graphene.Int()
    question = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateQuestionResponse(graphene.Mutation):
    class Arguments:
        input = QuestionResponseInput()

    questionResponse = graphene.Field(QuestionResponseType)

    @staticmethod
    def mutate(root, info, input=None):
        question = get_object_or_404(Question, pk=input.question)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        question_response_instance = QuestionResponse(
            title=input.title,
            question=question,
            serial_no=input.serial_no,
            reference_id=input.reference_id,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        question_response_instance.save()
        return CreateQuestionResponse(questionResponse=question_response_instance)


class MultiLanguageInput(graphene.InputObjectType):
    name = graphene.String()
    code = graphene.String()
    is_default = graphene.Boolean()


class CreateMultiLanguage(graphene.Mutation):
    class Arguments:
        input = MultiLanguageInput()

    multiLanguage = graphene.Field(MultiLanguageType)

    @staticmethod
    def mutate(self, root, info=None, input=None):
        multi_language_instanse = MultiLanguage(
            name=input.name,
            code=input.code,
            is_default=input.is_default
        )
        multi_language_instanse.save()
        return CreateMultiLanguage(multiLanguage=multi_language_instanse)


class UpdateMultiLanguageInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    code = graphene.String()
    is_default = graphene.Boolean()


class UpdateMultiLanguage(graphene.Mutation):
    class Arguments:
        input = UpdateMultiLanguageInput()

    multiLanguage = graphene.Field(MultiLanguageType)

    @staticmethod
    def mutate(self, root, info=None, input=None):
        multi_language_instanse = get_object_or_404(MultiLanguage, pk=input.id)
        if input.name:
            multi_language_instanse.name = input.name
        if input.code:
            multi_language_instanse.code = input.code
        if input.is_default:
            multi_language_instanse.is_default = input.is_default
        multi_language_instanse.save()
        return UpdateMultiLanguage(multiLanguage=multi_language_instanse)


class DeleteMultiLanguage(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    multiLanguage = graphene.Field(MultiLanguageType)

    @staticmethod
    def mutate(self, root, info=None, id=None):
        multi_language_instanse = get_object_or_404(MultiLanguage, pk=id)
        multi_language_instanse.delete()
        return DeleteMultiLanguage(multiLanguage=multi_language_instanse)


class CompanyLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    company = graphene.ID()
    code = graphene.String()
    name = graphene.String()
    street = graphene.String()
    street2 = graphene.String()
    state = graphene.String()
    city = graphene.String()
    zipcode = graphene.String()
    country = graphene.String()


class CreateCompanyLang(graphene.Mutation):
    class Arguments:
        input = CompanyLangInput()

    companyLang = graphene.Field(CompanyLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        company = Company.objects.get(pk=input.company)
        comapny_lang_instance = CompanyLang(
            lang=lang,
            company=company,
            code=input.code,
            name=input.name,
            street=input.street,
            street2=input.street2,
            state=input.state,
            city=input.city,
            zipcode=input.zipcode,
            country=input.country
        )
        comapny_lang_instance.save()
        return CreateCompanyLang(companyLang=comapny_lang_instance)


class UpdateCompanyLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    company = graphene.ID()
    code = graphene.String()
    name = graphene.String()
    street = graphene.String()
    street2 = graphene.String()
    state = graphene.String()
    city = graphene.String()
    zipcode = graphene.String()
    country = graphene.String()


class UpdateCompanyLang(graphene.Mutation):
    class Arguments:
        input = UpdateCompanyLangInput()

    companyLang = graphene.Field(CompanyLangType)

    @staticmethod
    def mutate(root, info, input=None):
        company_lang_instance = get_object_or_404(CompanyLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            company_lang_instance.lang = lang
        if input.company:
            company = Company.objects.get(pk=input.company)
            company_lang_instance.company = company
        if input.code:
            company_lang_instance.code = input.code
        if input.name:
            company_lang_instance.name = input.name
        if input.street:
            company_lang_instance.street = input.street
        if input.street2:
            company_lang_instance.street2 = input.street2
        if input.state:
            company_lang_instance.state = input.state
        if input.city:
            company_lang_instance.city = input.city
        if input.zipcode:
            company_lang_instance.zipcode = input.zipcode
        if input.country:
            company_lang_instance.country = input.country
        company_lang_instance.save()
        return UpdateCompanyLang(companyLang=company_lang_instance)


class DeleteCompanyLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    companyLang = graphene.Field(CompanyLangType)

    @staticmethod
    def mutate(root, info, id=None):
        company_lang_instance = get_object_or_404(CompanyLang, pk=id)
        company_lang_instance.delete()
        return DeleteCompanyLang(companyLang=company_lang_instance)


class DiagnosticLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    diagnostic = graphene.ID()
    name = graphene.String()


class CreateDiagnosticLang(graphene.Mutation):
    class Arguments:
        input = DiagnosticLangInput()

    diagnosticLang = graphene.Field(DiagnosticLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        diagnostic = Diagnostic.objects.get(pk=input.diagnostic)
        diagnostic_lang_instanse = DiagnosticLang(
            lang=lang,
            diagnostic=diagnostic,
            name=input.name
        )
        diagnostic_lang_instanse.save()
        return CreateDiagnosticLang(diagnosticLang=diagnostic_lang_instanse)


class UpdateDiagnosticLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    diagnostic = graphene.ID()
    name = graphene.String()


class UpdateDiagnosticLang(graphene.Mutation):
    class Arguments:
        input = UpdateDiagnosticLangInput()

    diagnosticLang = graphene.Field(DiagnosticLangType)

    @staticmethod
    def mutate(root, info, input=None):
        diagnostic_lang_instance = get_object_or_404(
            DiagnosticLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            diagnostic_lang_instance.lang = lang
        if input.diagnostic:
            diagnostic = Diagnostic.objects.get(pk=input.diagnostic)
            diagnostic_lang_instance.diagnostic = diagnostic
        if input.name:
            diagnostic_lang_instance.name = input.name
        diagnostic_lang_instance.save()
        return UpdateDiagnosticLang(diagnosticLang=diagnostic_lang_instance)


class DeleteDiagnosticLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    diagnosticLang = graphene.Field(DiagnosticLangType)

    @staticmethod
    def mutate(root, info, id=None):
        diagnostic_lang_instance = get_object_or_404(DiagnosticLang, pk=id)
        diagnostic_lang_instance.delete()
        return DeleteDiagnosticLang(diagnosticLang=diagnostic_lang_instance)


class TreatmentLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    treatment = graphene.ID()
    name = graphene.String()


class CreateTreatmentLang(graphene.Mutation):
    class Arguments:
        input = TreatmentLangInput()

    treatmentLang = graphene.Field(TreatmentLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        treatment = Treatment.objects.get(pk=input.treatment)
        treatment_lang_instanse = TreatmentLang(
            lang=lang,
            treatment=treatment,
            name=input.name
        )
        treatment_lang_instanse.save()
        return CreateTreatmentLang(treatmentLang=treatment_lang_instanse)


class UpdateTreatmentLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    treatment = graphene.ID()
    name = graphene.String()


class UpdateTreatmentLang(graphene.Mutation):
    class Arguments:
        input = UpdateTreatmentLangInput()

    treatmentLang = graphene.Field(TreatmentLangType)

    @staticmethod
    def mutate(root, info, input=None):
        treatment_lang_instance = get_object_or_404(TreatmentLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            treatment_lang_instance.lang = lang
        if input.treatment:
            treatment = Treatment.objects.get(pk=input.treatment)
            treatment_lang_instance.treatment = treatment
        if input.name:
            treatment_lang_instance.name = input.name
        treatment_lang_instance.save()
        return UpdateTreatmentLang(treatmentLang=treatment_lang_instance)


class DeleteTreatmentLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    treatmentLang = graphene.Field(TreatmentLangType)

    @staticmethod
    def mutate(root, info, id=None):
        treatment_lang_instance = get_object_or_404(TreatmentLang, pk=id)
        treatment_lang_instance.delete()
        return DeleteTreatmentLang(treatmentLang=treatment_lang_instance)


class SpecializationLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    specialization = graphene.ID()
    name = graphene.String()


class CreateSpecializationLang(graphene.Mutation):
    class Arguments:
        input = SpecializationLangInput()

    specializationLang = graphene.Field(SpecializationLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        specialization = Specialization.objects.get(pk=input.specialization)
        specialization_lang_instanse = SpecializationLang(
            lang=lang,
            specialization=specialization,
            name=input.name
        )
        specialization_lang_instanse.save()
        return CreateSpecializationLang(specializationLang=specialization_lang_instanse)


class UpdateSpecializationLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    specialization = graphene.ID()
    name = graphene.String()


class UpdateSpecializationLang(graphene.Mutation):
    class Arguments:
        input = UpdateSpecializationLangInput()

    specializationLang = graphene.Field(SpecializationLangType)

    @staticmethod
    def mutate(root, info, input=None):
        specialization_lang_instance = get_object_or_404(
            SpecializationLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            specialization_lang_instance.lang = lang
        if input.specialization:
            specialization = Specialization.objects.get(
                pk=input.specialization)
            specialization_lang_instance.specialization = specialization
        if input.name:
            specialization_lang_instance.name = input.name
        specialization_lang_instance.save()
        return UpdateSpecializationLang(specializationLang=specialization_lang_instance)


class DeleteSpecializationLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    specializationLang = graphene.Field(SpecializationLangType)

    @staticmethod
    def mutate(root, info, id=None):
        specialization_lang_instance = get_object_or_404(
            SpecializationLang, pk=id)
        specialization_lang_instance.delete()
        return DeleteSpecializationLang(specializationLang=specialization_lang_instance)


class QuestionLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    question = graphene.ID()
    title = graphene.String()


class CreateQuestionLang(graphene.Mutation):
    class Arguments:
        input = QuestionLangInput()

    questionLang = graphene.Field(QuestionLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        question = Question.objects.get(pk=input.question)
        question_lang_instanse = QuestionLang(
            lang=lang,
            question=question,
            title=input.title
        )
        question_lang_instanse.save()
        return CreateQuestionLang(questionLang=question_lang_instanse)


class UpdateQuestionLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    question = graphene.ID()
    title = graphene.String()


class UpdateQuestionLang(graphene.Mutation):
    class Arguments:
        input = UpdateQuestionLangInput()

    questionLang = graphene.Field(QuestionLangType)

    @staticmethod
    def mutate(root, info, input=None):
        question_lang_instance = get_object_or_404(QuestionLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            question_lang_instance.lang = lang
        if input.question:
            question = Question.objects.get(pk=input.question)
            question_lang_instance.question = question
        if input.title:
            question_lang_instance.title = input.title
        question_lang_instance.save()
        return UpdateQuestionLang(questionLang=question_lang_instance)


class DeleteQuestionLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    questionLang = graphene.Field(QuestionLangType)

    @staticmethod
    def mutate(root, info, id=None):
        question_lang_instance = get_object_or_404(QuestionLang, pk=id)
        question_lang_instance.delete()
        return DeleteQuestionLang(questionLang=question_lang_instance)


class QuestionResponseLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    question_response = graphene.ID()
    title = graphene.String()


class CreateQuestionResponseLang(graphene.Mutation):
    class Arguments:
        input = QuestionResponseLangInput()

    questionResponseLang = graphene.Field(QuestionResponseLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        question_response = QuestionResponse.objects.get(
            pk=input.question_response)
        question_response_lang_instanse = QuestionResponseLang(
            lang=lang,
            question_response=question_response,
            title=input.title
        )
        question_response_lang_instanse.save()
        return CreateQuestionResponseLang(questionResponseLang=question_response_lang_instanse)


class UpdateQuestionResponseLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    question_response = graphene.ID()
    title = graphene.String()


class UpdateQuestionResponseLang(graphene.Mutation):
    class Arguments:
        input = UpdateQuestionResponseLangInput()

    questionResponseLang = graphene.Field(QuestionResponseLangType)

    @staticmethod
    def mutate(root, info, input=None):
        question_response_lang_instance = get_object_or_404(
            QuestionResponseLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            question_response_lang_instance.lang = lang
        if input.question_response:
            question_response = QuestionResponse.objects.get(
                pk=input.question_response)
            question_response_lang_instance.question_response = question_response
        if input.title:
            question_response_lang_instance.title = input.title
        question_response_lang_instance.save()
        return UpdateQuestionResponseLang(questionResponseLang=question_response_lang_instance)


class DeleteQuestionResponseLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    questionResponseLang = graphene.Field(QuestionResponseLangType)

    @staticmethod
    def mutate(root, info, id):
        question_response_lang_instance = get_object_or_404(
            QuestionResponseLang, pk=id)
        question_response_lang_instance.delete()
        return DeleteQuestionResponseLang(questionResponseLang=question_response_lang_instance)


class QualificationLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    qualification = graphene.ID()
    name = graphene.String()


class CreateQualificationLang(graphene.Mutation):
    class Arguments:
        input = QualificationLangInput()

    qualificationLang = graphene.Field(QualificationLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        qualification = Qualification.objects.get(pk=input.qualification)
        qualification_lang_instanse = QualificationLang(
            lang=lang,
            qualification=qualification,
            name=input.name
        )
        qualification_lang_instanse.save()
        return CreateQualificationLang(qualificationLang=qualification_lang_instanse)


class UpdateQualificationLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    qualification = graphene.ID()
    name = graphene.String()


class UpdateQualificationLang(graphene.Mutation):
    class Arguments:
        input = UpdateQualificationLangInput()

    qualificationLang = graphene.Field(QualificationLangType)

    @staticmethod
    def mutate(root, info, input=None):
        qualification_lang_instance = get_object_or_404(
            QualificationLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            qualification_lang_instance.lang = lang
        if input.qualification:
            qualification = Qualification.objects.get(pk=input.qualification)
            qualification_lang_instance.qualification = qualification
        if input.name:
            qualification_lang_instance.name = input.name
        qualification_lang_instance.save()
        return UpdateQualificationLang(qualificationLang=qualification_lang_instance)


class DeleteQualificationLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    qualificationLang = graphene.Field(QualificationLangType)

    @staticmethod
    def mutate(root, info, id):
        qualification_lang_instance = get_object_or_404(
            QualificationLang, pk=id)
        qualification_lang_instance.delete()
        return DeleteQualificationLang(qualificationLang=qualification_lang_instance)


class PriorityLangInput(graphene.InputObjectType):
    lang = graphene.ID()
    priority = graphene.ID()
    name = graphene.String()


class CreatePriorityLang(graphene.Mutation):
    class Arguments:
        input = PriorityLangInput()

    priorityLang = graphene.Field(PriorityLangType)

    @staticmethod
    def mutate(root, info, input=None):
        lang = MultiLanguage.objects.get(pk=input.lang)
        priority = Priority.objects.get(pk=input.priority)
        priority_lang_instanse = PriorityLang(
            lang=lang,
            priority=priority,
            name=input.name
        )
        priority_lang_instanse.save()
        return CreatePriorityLang(priorityLang=priority_lang_instanse)


class UpdatePriorityLangInput(graphene.InputObjectType):
    id = graphene.ID()
    lang = graphene.ID()
    priority = graphene.ID()
    name = graphene.String()


class UpdatePriorityLang(graphene.Mutation):
    class Arguments:
        input = UpdatePriorityLangInput()

    priorityLang = graphene.Field(PriorityLangType)

    @staticmethod
    def mutate(root, info, input=None):
        priority_lang_instance = get_object_or_404(PriorityLang, pk=input.id)
        if input.lang:
            lang = MultiLanguage.objects.get(pk=input.lang)
            priority_lang_instance.lang = lang
        if input.priority:
            priority = Priority.objects.get(pk=input.priority)
            priority_lang_instance.priority = priority
        if input.name:
            priority_lang_instance.name = input.name
        priority_lang_instance.save()
        return UpdatePriorityLang(priorityLang=priority_lang_instance)


class DeletePriorityLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    priorityLang = graphene.Field(PriorityLangType)

    @staticmethod
    def mutate(root, info, id):
        priority_lang_instance = get_object_or_404(PriorityLang, pk=id)
        priority_lang_instance.delete()
        return DeletePriorityLang(priorityLang=priority_lang_instance)


class AppointmentCodeInput(graphene.InputObjectType):
    code_type = graphene.String()
    code = graphene.String()
    name = graphene.String()
    description = graphene.String()


class CreateAppointmentCode(graphene.Mutation):
    class Arguments:
        input = AppointmentCodeInput()

    appointmentCode = graphene.Field(AppointmentCodeType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment_code_instanse = AppointmentCode(
            code_type=input.code_type,
            code=input.code,
            name=input.name,
            description=input.description
        )
        appointment_code_instanse.save()
        return CreateAppointmentCode(appointmentCode=appointment_code_instanse)


class UpdateAppointmentCodeInput(graphene.InputObjectType):
    id = graphene.ID()
    code_type = graphene.String()
    code = graphene.String()
    name = graphene.String()
    description = graphene.String()


class UpdateAppointmentCode(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentCodeInput()

    appointmentCode = graphene.Field(AppointmentCodeType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment_code_instance = get_object_or_404(
            AppointmentCode, pk=input.id)
        if input.code_type:
            appointment_code_instance.code_type = input.code_type
        if input.code:
            appointment_code_instance.code = input.code
        if input.name:
            appointment_code_instance.name = input.name
        if input.description:
            appointment_code_instance.description = input.description
        appointment_code_instance.save()
        return UpdateAppointmentCode(appointmentCode=appointment_code_instance)


class DeleteAppointmentCode(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointmentCode = graphene.Field(AppointmentCodeType)

    @staticmethod
    def mutate(root, info, id):
        appointment_code_instance = get_object_or_404(AppointmentCode, pk=id)
        appointment_code_instance.delete()
        return DeleteAppointmentCode(appointmentCode=appointment_code_instance)


class Mutation(graphene.ObjectType):
    create_duration = DurationCreate.Field()
    create_tooth = CreateTooth.Field()
    create_diagnostic = CreateDiagnostic.Field()
    create_treatment = CreateTreatment.Field()
    create_specialization = CreateSpecialization.Field()
    delete_specialization = DeleteSpecialization.Field()
    create_company = CreateCompany.Field()
    update_company = UpdateCompany.Field()
    create_company_user = CreateCompanyUser.Field()
    update_company_user = UpdateCompanyUser.Field()
    delete_company_user = DeleteCompanyUser.Field()
    create_question = CreateQuestion.Field()
    create_question_response = CreateQuestionResponse.Field()
    create_multi_lang = CreateMultiLanguage.Field()
    update_multi_lang = UpdateMultiLanguage.Field()
    delete_multi_lang = DeleteMultiLanguage.Field()
    create_company_lang = CreateCompanyLang.Field()
    update_company_lang = UpdateCompanyLang.Field()
    delete_company_lang = DeleteCompanyLang.Field()
    create_diagnostic_lang = CreateDiagnosticLang.Field()
    update_diagnostic_lang = UpdateDiagnosticLang.Field()
    delete_diagnostic_lang = DeleteDiagnosticLang.Field()
    create_treatment_lang = CreateTreatmentLang.Field()
    update_treatment_lang = UpdateTreatmentLang.Field()
    delete_treratment_lang = DeleteTreatmentLang.Field()
    create_specialization_lang = CreateSpecializationLang.Field()
    update_specialization_lang = UpdateSpecializationLang.Field()
    delete_specialization_lang = DeleteSpecializationLang.Field()
    create_question_lang = CreateQuestionLang.Field()
    update_question_lang = UpdateQuestionLang.Field()
    delete_question_lang = DeleteQuestionLang.Field()
    create_question_response_lang = CreateQuestionResponseLang.Field()
    update_question_response_lang = UpdateQuestionResponseLang.Field()
    delete_question_response_lang = DeleteQuestionResponseLang.Field()
    create_qualification_lang = CreateQualificationLang.Field()
    update_qualification_lang = UpdateQualificationLang.Field()
    delete_qualification_lang = DeleteQualificationLang.Field()
    create_priority_lang = CreatePriorityLang.Field()
    update_priority_lang = UpdatePriorityLang.Field()
    delete_priority_lang = DeletePriorityLang.Field()
    create_appointment_code = CreateAppointmentCode.Field()
    update_appointment_code = UpdateAppointmentCode.Field()
    delete_appointment_code = DeleteAppointmentCode.Field()
