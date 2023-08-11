import graphene
from api.models.user_model import User
from common.handle_error import get_object_or_None
from common.models import *
from django.shortcuts import get_object_or_404
from graphene_file_upload.scalars import Upload
from .models import *
from .types import *
from api.models.user_model import MultiLanguage


class AppointmentInput(graphene.InputObjectType):
    patient = graphene.ID()
    doctor = graphene.ID()
    company = graphene.ID()
    start_date = graphene.DateTime()
    duration = graphene.Int()
    note = graphene.String()
    is_deleted = graphene.Boolean()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointment(graphene.Mutation):
    class Arguments:
        input = AppointmentInput()

    appointment = graphene.Field(AppointmentType)

    @staticmethod
    def mutate(root, info, input=None):
        patient = User.objects.get(pk=input.patient)
        doctor = User.objects.get(pk=input.doctor)
        company = Company.objects.get(pk=input.company)
        created_by = User.objects.get(pk=input.created_by)
        updated_by = User.objects.get(pk=input.updated_by)
        appointment_instance = Appointment(
            patient=patient,
            doctor=doctor,
            company=company,
            start_date=input.start_date,
            duration=input.duration,
            note=input.note,
            is_deleted=input.is_deleted,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_instance.save()
        return CreateAppointment(appointment=appointment_instance)


class AppointmentUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    patient = graphene.ID()
    doctor = graphene.ID()
    company = graphene.ID()
    start_date = graphene.DateTime()
    duration = graphene.Int()
    note = graphene.String()
    is_deleted = graphene.Boolean()
    updated_by = graphene.ID()


class UpdateAppointment(graphene.Mutation):
    class Arguments:
        input = AppointmentUpdateInput()

    appointment = graphene.Field(AppointmentType)

    @staticmethod
    def mutate(root, info, input=None):
        patient = get_object_or_404(User, pk=input.patient)
        doctor = get_object_or_404(User, pk=input.doctor)
        company = get_object_or_404(Company, pk=input.company)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        appointment_instance = Appointment.objects.get(pk=input.id)
        if appointment_instance:
            appointment_instance.patient = patient
            appointment_instance.doctor = doctor
            appointment_instance.company = company
            appointment_instance.start_date = input.start_date
            appointment_instance.duration = input.duration
            appointment_instance.note = input.note
            appointment_instance.is_deleted = input.is_deleted
            appointment_instance.updated_by = updated_by
            appointment_instance.save()
            return UpdateAppointment(appointment=appointment_instance)
        return UpdateAppointment(appointment=None)


class DeleteAppointment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointment = graphene.Field(AppointmentType)

    @staticmethod
    def mutate(root, info, id):
        appointment_instance = get_object_or_404(Appointment, pk=id)
        appointment_instance.delete()
        return None


class AppointmentDetailsInput(graphene.InputObjectType):
    appointment = graphene.ID()
    tooth = graphene.ID()
    diagnosis = graphene.ID()
    treatment = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentDetails(graphene.Mutation):
    class Arguments:
        input = AppointmentDetailsInput()

    appointment_details = graphene.Field(AppointmentDetailType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        tooth = get_object_or_None(Tooth, pk=input.tooth)
        diagnosis = get_object_or_None(Diagnostic, pk=input.diagnosis)
        treatment = get_object_or_None(Treatment, pk=input.treatment)
        created_by = User.objects.get(pk=input.created_by)
        updated_by = User.objects.get(pk=input.updated_by)
        appointment_details_instance = AppointmentDetail(
            appointment=appointment,
            tooth=tooth,
            diagnosis=diagnosis,
            treatment=treatment,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_details_instance.save()
        return CreateAppointmentDetails(appointment_details=appointment_details_instance)


class UpdateAppointmentDetailsInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    tooth = graphene.ID()
    diagnosis = graphene.ID()
    treatment = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentDetails(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentDetailsInput()

    appointment_details = graphene.Field(AppointmentDetailType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        tooth = get_object_or_None(Tooth, pk=input.tooth)
        diagnosis = get_object_or_None(Diagnostic, pk=input.diagnosis)
        treatment = get_object_or_None(Treatment, pk=input.treatment)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        appointment_details_instance = AppointmentDetail.objects.get(
            pk=input.id)
        if appointment_details_instance:
            appointment_details_instance.appointment = appointment
            appointment_details_instance.tooth = tooth
            appointment_details_instance.diagnosis = diagnosis
            appointment_details_instance.treatment = treatment
            appointment_details_instance.updated_by = updated_by
            appointment_details_instance.save()
            return UpdateAppointmentDetails(appointment_details=appointment_details_instance)
        return UpdateAppointmentDetails(appointment_details=None)


class DeleteAppointmentDetails(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointment = graphene.Field(AppointmentDetailType)

    @staticmethod
    def mutate(root, info, id):
        appointment_instance = get_object_or_404(AppointmentDetail, pk=id)
        appointment_instance.delete()
        return None


class AppointmentPriortiyInput(graphene.InputObjectType):
    appointment = graphene.ID()
    priority = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentPriortiy(graphene.Mutation):
    class Arguments:
        input = AppointmentPriortiyInput()

    appointment_priority = graphene.Field(AppointmentProrityType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        priority = get_object_or_404(Priority, pk=input.priority)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_priority_instance = AppointmentPriority(
            appointment=appointment,
            priority=priority,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_priority_instance.save()
        return CreateAppointmentPriortiy(appointment_priority=appointment_priority_instance)


class UpdateAppointmentPriortiyInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    priority = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentPriortiy(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentPriortiyInput()

    appointment_priority = graphene.Field(AppointmentProrityType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        priority = get_object_or_404(Priority, pk=input.priority)
        created_by = get_object_or_None(User, pk=input.created_by)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        appointment_priority_instance = AppointmentPriority.objects.get(
            pk=input.id)
        if appointment_priority_instance:
            appointment_priority_instance.appointment = appointment
            appointment_priority_instance.priority = priority
            appointment_priority_instance.created_by = created_by
            appointment_priority_instance.updated_by = updated_by or created_by
            appointment_priority_instance.save()
            return UpdateAppointmentPriortiy(appointment_priority=appointment_priority_instance)
        return UpdateAppointmentPriortiy(appointment_priority=None)


class DeleteAppointmentPriority(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointment_priority = graphene.Field(AppointmentProrityType)

    @staticmethod
    def mutate(root, info, id):
        appointment_priority_instance = get_object_or_404(
            AppointmentPriority, pk=id)
        appointment_priority_instance.delete()
        return None


class AppointmentSpecializationInput(graphene.InputObjectType):
    appointment = graphene.ID()
    specialization = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentSpecialization(graphene.Mutation):
    class Arguments:
        input = AppointmentSpecializationInput()

    appointment_specialization = graphene.Field(AppointmentSpecializationType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        specialization = get_object_or_404(
            Specialization, pk=input.specialization)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_specialization_instance = AppointmentSpecialization(
            appointment=appointment,
            specialization=specialization,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_specialization_instance.save()
        return CreateAppointmentSpecialization(appointment_specialization=appointment_specialization_instance)


class UpdateAppointmentSpecializationInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    specialization = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentSpecialization(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentSpecializationInput()

    appointment_specialization = graphene.Field(AppointmentSpecializationType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        specialization = get_object_or_404(
            Specialization, pk=input.specialization)
        created_by = get_object_or_None(User, pk=input.created_by)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        appointment_specialization_instance = AppointmentSpecialization.objects.get(
            pk=input.id)
        if appointment_specialization_instance:
            appointment_specialization_instance.appointment = appointment
            appointment_specialization_instance.specialization = specialization
            appointment_specialization_instance.created_by = created_by
            appointment_specialization_instance.updated_by = updated_by or created_by
            appointment_specialization_instance.save()
            return UpdateAppointmentSpecialization(appointment_specialization=appointment_specialization_instance)
        return UpdateAppointmentSpecialization(appointment_specialization=None)


class DeleteAppointmentSpecialization(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointment_specialization = graphene.Field(AppointmentSpecializationType)

    @staticmethod
    def mutate(root, info, id):
        appointment_specialization_instance = get_object_or_404(
            AppointmentSpecialization, pk=id)
        appointment_specialization_instance.delete()
        return None


class DiseaseInput(graphene.InputObjectType):
    user = graphene.ID()
    question = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateDisease(graphene.Mutation):
    class Arguments:
        input = DiseaseInput()

    disease = graphene.Field(DiseaseType)

    @staticmethod
    def mutate(root, info, input=None):
        question = get_object_or_404(Question, pk=input.question)
        user = get_object_or_404(User, pk=input.user)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        disease_instance = Disease(
            question=question,
            user=user,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        disease_instance.save()
        return CreateDisease(disease=disease_instance)


class DiseaseUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    user = graphene.ID()
    question = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateDisease(graphene.Mutation):
    class Arguments:
        input = DiseaseUpdateInput()

    disease = graphene.Field(DiseaseType)

    @staticmethod
    def mutate(root, info, input=None):
        question = get_object_or_404(Question, pk=input.question)
        user = get_object_or_404(User, pk=input.user)
        created_by = get_object_or_None(User, pk=input.created_by)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        update_disease_instance = Disease.objects.get(pk=input.id)
        if update_disease_instance:
            update_disease_instance.question = question
            update_disease_instance.user = user
            update_disease_instance.created_by = created_by
            update_disease_instance.updated_by = updated_by or created_by
            update_disease_instance.save()
        return UpdateDisease(disease=update_disease_instance)


class DiseaseAnswerInput(graphene.InputObjectType):
    value = graphene.String()
    disease = graphene.ID()
    questionResponse = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateDiseaseAnswer(graphene.Mutation):
    class Arguments:
        input = DiseaseAnswerInput()

    diseaseAnswer = graphene.Field(DiseaseAnswerType)

    @staticmethod
    def mutate(root, info, input=None):
        disease = get_object_or_404(Disease, pk=input.disease)
        questionResponse = get_object_or_None(
            QuestionResponse, pk=input.questionResponse)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        disease_answer_instance = DiseaseAnswer(
            value=input.value,
            disease=disease,
            questionResponse=questionResponse,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        disease_answer_instance.save()
        return CreateDiseaseAnswer(diseaseAnswer=disease_answer_instance)


class DiseaseAnswerUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    value = graphene.String()
    disease = graphene.ID()
    questionResponse = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateDiseaseAnswer(graphene.Mutation):
    class Arguments:
        input = DiseaseAnswerUpdateInput()

    diseaseAnswer = graphene.Field(DiseaseAnswerType)

    @staticmethod
    def mutate(root, info, input=None):
        disease = get_object_or_404(Disease, pk=input.disease)
        questionResponse = get_object_or_None(
            QuestionResponse, pk=input.questionResponse)
        created_by = get_object_or_None(User, pk=input.created_by)
        updated_by = get_object_or_404(User, pk=input.updated_by)
        update_disease_answer_instance = DiseaseAnswer.objects.get(pk=input.id)
        if update_disease_answer_instance:
            update_disease_answer_instance.value = input.value
            update_disease_answer_instance.disease = disease
            update_disease_answer_instance.questionResponse = questionResponse
            update_disease_answer_instance.created_by = created_by
            update_disease_answer_instance.updated_by = updated_by or created_by
            update_disease_answer_instance.save()
        return UpdateDiseaseAnswer(diseaseAnswer=update_disease_answer_instance)


class DeleteDiseaseAnswer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    diseaseAnswer = graphene.Field(DiseaseAnswerType)

    @staticmethod
    def mutate(root, info, id):
        delete_disease_answer_instance = get_object_or_404(
            DiseaseAnswer, pk=id)
        delete_disease_answer_instance.delete()
        return None


class DeleteUserDisease(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    disease = graphene.Field(DiseaseType)

    @staticmethod
    def mutate(root, info, id):
        delete_disease_instance = Disease.objects.filter(user__id=id)
        delete_disease_instance.delete()
        return None


class DeleteDisease(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    disease = graphene.Field(DiseaseType)

    @staticmethod
    def mutate(root, info, id):
        delete_disease_instance = get_object_or_404(Disease, pk=id)
        delete_disease_instance.delete()
        return None


class AppointmentFileInput(graphene.InputObjectType):
    name = graphene.String()
    file = Upload()
    appointment = graphene.ID()
    doctor = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentFile(graphene.Mutation):
    class Arguments:
        input = AppointmentFileInput()

    appointmentFile = graphene.Field(AppointmentFileType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        doctor = get_object_or_404(User, pk=input.doctor)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_file_instance = AppointmentFile(
            name=input.name,
            file=input.file,
            appointment=appointment,
            doctor=doctor,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_file_instance.save()
        return CreateAppointmentFile(appointmentFile=appointment_file_instance)


class AppointmentSurveyInput(graphene.InputObjectType):
    appointment = graphene.ID()
    survey = graphene.ID()
    is_finished = graphene.Boolean()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentSurvey(graphene.Mutation):
    class Arguments:
        input = AppointmentSurveyInput()

    appointmentSurvey = graphene.Field(AppointmentSurveyType)

    @staticmethod
    def mutate(root, info, input=None):
        survey = get_object_or_404(Survey, pk=input.survey)
        is_finished = input.is_finished
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_survey_instance = AppointmentSurvey(
            survey=survey,
            is_finished=is_finished,
            appointment=appointment,
            created_by=created_by,
            updated_by=updated_by or created_by,
        )
        appointment_survey_instance.save()
        return CreateAppointmentSurvey(appointmentSurvey=appointment_survey_instance)


class AppointmentSurveyUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    survey = graphene.ID()
    is_finished = graphene.Boolean()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentSurvey(graphene.Mutation):
    class Arguments:
        input = AppointmentSurveyUpdateInput()

    appointmentSurvey = graphene.Field(AppointmentSurveyType)

    @staticmethod
    def mutate(root, info, input=None):
        survey = get_object_or_404(Survey, pk=input.survey)
        is_finished = input.is_finished
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        update_appointment_survey_instance = AppointmentSurvey.objects.get(
            pk=input.id)
        if update_appointment_survey_instance:
            update_appointment_survey_instance.survey = survey
            update_appointment_survey_instance.appointment = appointment
            update_appointment_survey_instance.is_finished = is_finished
            update_appointment_survey_instance.created_by = created_by
            update_appointment_survey_instance.updated_by = updated_by or created_by
            update_appointment_survey_instance.save()
        return UpdateAppointmentSurvey(appointmentSurvey=update_appointment_survey_instance)


class DeleteAppointmentSurvey(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointmentSurvey = graphene.Field(AppointmentSurveyType)

    @staticmethod
    def mutate(root, info, id):
        delete_appointment_survey_instance = get_object_or_404(
            AppointmentSurvey, id=id)
        delete_appointment_survey_instance.delete()
        return None


class AppointmentSurveyQuestionResponseInput(graphene.InputObjectType):
    appointment_survey = graphene.ID()
    response_value = graphene.String()
    survey_question = graphene.ID()
    question_response = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentSurveyQuestionResponse(graphene.Mutation):
    class Arguments:
        input = AppointmentSurveyQuestionResponseInput()

    appointmentSurveyQuestionResponse = graphene.Field(
        AppointmentSurveyQuestionResponseType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment_survey = get_object_or_404(
            AppointmentSurvey, pk=input.appointment_survey)
        survey_question = get_object_or_404(
            SurveysQuestion, pk=input.survey_question)
        if input.question_response and input.question_response != "null":
            question_response = get_object_or_404(
                SurveyQuestionResponse, pk=input.question_response)
            text = question_response.question_response
        else:
            question_response = None
            text = input.response_value
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_survey_question_response_instance = AppointmentSurveyQuestionResponse(
            appointment_survey=appointment_survey,
            survey_question=survey_question,
            question_response=question_response,
            created_by=created_by,
            updated_by=updated_by or created_by,
            response_value=text
        )
        appointment_survey_question_response_instance.save()
        return CreateAppointmentSurveyQuestionResponse(appointmentSurveyQuestionResponse=appointment_survey_question_response_instance)


class AppointmentSurveyQuestionResponseUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment_survey = graphene.ID()
    survey_question = graphene.ID()
    response_value = graphene.String()
    question_response = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentSurveyQuestionResponse(graphene.Mutation):
    class Arguments:
        input = AppointmentSurveyQuestionResponseUpdateInput()

    appointmentSurveyQuestionResponse = graphene.Field(
        AppointmentSurveyQuestionResponseType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment_survey = get_object_or_404(
            AppointmentSurvey, pk=input.appointment_survey)
        survey_question = get_object_or_404(
            SurveysQuestion, pk=input.survey_question)
        if input.question_response and input.question_response != "null":
            question_response = get_object_or_404(
                SurveyQuestionResponse, pk=input.question_response)
            text = question_response.question_response
        else:
            question_response = None
            text = input.response_value
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        update_appointment_survey_question_response_instance = AppointmentSurveyQuestionResponse.objects.get(
            pk=input.id)
        if update_appointment_survey_question_response_instance:
            update_appointment_survey_question_response_instance.appointment_survey = appointment_survey
            update_appointment_survey_question_response_instance.survey_question = survey_question
            update_appointment_survey_question_response_instance.question_response = question_response
            update_appointment_survey_question_response_instance.response_value = text
            update_appointment_survey_question_response_instance.created_by = created_by
            update_appointment_survey_question_response_instance.updated_by = updated_by or created_by
            update_appointment_survey_question_response_instance.save()
        return UpdateAppointmentSurveyQuestionResponse(appointmentSurveyQuestionResponse=update_appointment_survey_question_response_instance)


class DeleteAppointmentSurveyQuestionResponse(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    appointmentSurveyQuestionResponse = graphene.Field(
        AppointmentSurveyQuestionResponseType)

    @staticmethod
    def mutate(root, info, id):
        delete_appointment_survey_question_response_instance = get_object_or_404(
            AppointmentSurveyQuestionResponse, id=id)
        delete_appointment_survey_question_response_instance.delete()
        return None


class AppointmentLangInput(graphene.InputObjectType):
    appointment = graphene.ID()
    lang = graphene.ID()
    note = graphene.String()


class CreateAppointmentLang(graphene.Mutation):
    class Arguments:
        input = AppointmentLangInput()

    appointmentLang = graphene.Field(AppointmentLangType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        lang = get_object_or_404(MultiLanguage, pk=input.lang)
        note = input.note
        appointment_lang_instance = AppointmentLang(
            appointment=appointment,
            lang=lang,
            note=note
        )
        appointment_lang_instance.save()
        return CreateAppointmentLang(appointmentLang=appointment_lang_instance)


class UpdateAppointmentLangInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    lang = graphene.ID()
    note = graphene.String()


class UpdateAppointmentLang(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentLangInput()

    appointmentLang = graphene.Field(AppointmentLangType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        lang = get_object_or_404(MultiLanguage, pk=input.lang)
        note = input.note
        update_appointment_lang_instance = AppointmentLang.objects.get(
            pk=input.id)
        if update_appointment_lang_instance:
            update_appointment_lang_instance.appointment = appointment
            update_appointment_lang_instance.lang = lang
            update_appointment_lang_instance.note = note
            update_appointment_lang_instance.save()
        return UpdateAppointmentLang(appointmentLang=update_appointment_lang_instance)


class DeleteAppointmentLang(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointmentLang = graphene.Field(AppointmentLangType)

    @staticmethod
    def mutate(root, info, id):
        delete_appointment_lang_instance = get_object_or_404(
            AppointmentLang, id=id)
        delete_appointment_lang_instance.delete()
        return None


class AppointmentShortCodeInput(graphene.InputObjectType):
    appointment = graphene.ID()
    appointment_code = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateAppointmentShortCode(graphene.Mutation):
    class Arguments:
        input = AppointmentShortCodeInput()

    appointmentShortCode = graphene.Field(AppointmentShortCodeType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        appointment_code = get_object_or_404(
            AppointmentCode, pk=input.appointment_code)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        appointment_short_code_instance = AppointmentShortCode(
            appointment=appointment,
            appointment_code=appointment_code,
            created_by=created_by,
            updated_by=updated_by or created_by
        )
        appointment_short_code_instance.save()
        return CreateAppointmentShortCode(appointmentShortCode=appointment_short_code_instance)


class UpdateAppointmentShortCodeInput(graphene.InputObjectType):
    id = graphene.ID()
    appointment = graphene.ID()
    appointment_code = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class UpdateAppointmentShortCode(graphene.Mutation):
    class Arguments:
        input = UpdateAppointmentShortCodeInput()

    appointmentShortCode = graphene.Field(AppointmentShortCodeType)

    @staticmethod
    def mutate(root, info, input=None):
        appointment = get_object_or_404(Appointment, pk=input.appointment)
        appointment_code = get_object_or_404(
            AppointmentCode, pk=input.appointment_code)
        created_by = get_object_or_404(User, pk=input.created_by)
        updated_by = get_object_or_None(User, pk=input.updated_by)
        update_appointment_short_code_instance = AppointmentShortCode.objects.get(
            pk=input.id)
        if update_appointment_short_code_instance:
            update_appointment_short_code_instance.appointment = appointment
            update_appointment_short_code_instance.appointment_code = appointment_code
            update_appointment_short_code_instance.created_by = created_by
            update_appointment_short_code_instance.updated_by = updated_by or created_by
            update_appointment_short_code_instance.save()
        return UpdateAppointmentShortCode(appointmentShortCode=update_appointment_short_code_instance)


class DeleteAppointmentShortCode(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    appointmentShortCode = graphene.Field(AppointmentShortCodeType)

    @staticmethod
    def mutate(root, info, id):
        delete_appointment_short_code_instance = get_object_or_404(
            AppointmentShortCode, id=id)
        delete_appointment_short_code_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
    update_appointment = UpdateAppointment.Field()
    delete_appointment = DeleteAppointment.Field()
    create_appointment_details = CreateAppointmentDetails.Field()
    update_appointment_details = UpdateAppointmentDetails.Field()
    delete_appointment_details = DeleteAppointmentDetails.Field()
    create_appointment_priority = CreateAppointmentPriortiy.Field()
    update_appointment_priority = UpdateAppointmentPriortiy.Field()
    delete_appointment_priority = DeleteAppointmentPriority.Field()
    create_appointment_specialization = CreateAppointmentSpecialization.Field()
    update_appointment_specialization = UpdateAppointmentSpecialization.Field()
    delete_appointment_specialization = DeleteAppointmentSpecialization.Field()
    create_disease = CreateDisease.Field()
    update_disease = UpdateDisease.Field()
    create_disease_answer = CreateDiseaseAnswer.Field()
    update_disease_answer = UpdateDiseaseAnswer.Field()
    delete_disease_answer = DeleteDiseaseAnswer.Field()
    delete_user_disease = DeleteUserDisease.Field()
    delete_disease = DeleteDisease.Field()
    create_appointment_file = CreateAppointmentFile.Field()
    create_appointment_survey = CreateAppointmentSurvey.Field()
    update_appointment_survey = UpdateAppointmentSurvey.Field()
    delete_appointment_survey = DeleteAppointmentSurvey.Field()
    create_appointment_survey_question_response = CreateAppointmentSurveyQuestionResponse.Field()
    update_appointment_survey_question_response = UpdateAppointmentSurveyQuestionResponse.Field()
    delete_appointment_survey_question_response = DeleteAppointmentSurveyQuestionResponse.Field()
    create_appointment_lang = CreateAppointmentLang.Field()
    update_appointment_lang = UpdateAppointmentLang.Field()
    delete_appointment_lang = DeleteAppointmentLang.Field()
    create_appointment_short_code = CreateAppointmentShortCode.Field()
    update_appointment_short_code = UpdateAppointmentShortCode.Field()
    delete_appointment_short_code = DeleteAppointmentShortCode.Field()
