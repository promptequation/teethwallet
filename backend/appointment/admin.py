import xml.etree.ElementTree as ET
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.urls import reverse
from django.db.transaction import atomic
from appointment.models import *
from django.urls import resolve


class AppointmentFollowUpInline(admin.TabularInline):
    model = AppointmentFollowUp
    extra = 0
    fields = ('diagnosis', 'treatment', 'follow_up_date',)

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            appointment = Appointment.objects.get(
                pk=self.get_parent_object_from_request(request).id)
            appointment_details = AppointmentDetail.objects.filter(
                appointment=appointment)
            diagnosis_id = []
            for appointment_detail in appointment_details:
                diagnosis_id.append(appointment_detail.diagnosis.id)
            treatment_id = []
            for appointment_detail in appointment_details:
                treatment_id.append(appointment_detail.treatment.id)
            if db_field.name == "diagnosis":
                kwargs["queryset"] = Diagnostic.objects.filter(
                    id__in=diagnosis_id)
            if db_field.name == "treatment":
                kwargs["queryset"] = Treatment.objects.filter(
                    id__in=treatment_id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        except:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", 'company', 'start_date', "duration",
                    'is_deleted', "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('patient__first_name',
                     "doctor__first_name", "company__name")
    inlines = [AppointmentFollowUpInline, ]


@admin.register(AppointmentDetail)
class AppointmentDetailAdmin(admin.ModelAdmin):
    list_display = ("appointment", "doctor_name", "patient_name", "tooth", 'diagnosis',
                    "treatment", "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('appointment__doctor__first_name',
                     'appointment__patient__first_name', "treatment__name")

    def doctor_name(self, appointment_details):
        return appointment_details.appointment.doctor

    def patient_name(self, appointment_details):
        return appointment_details.appointment.patient


@admin.register(AppointmentPriority)
class AppointmentPriorityAdmin(admin.ModelAdmin):
    list_display = ("appointment", "doctor_name", "patient_name", "priority", "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('appointment__doctor__first_name',
                     'appointment__patient__first_name', "priority__name")

    def doctor_name(self, appointment_details):
        return appointment_details.appointment.doctor

    def patient_name(self, appointment_details):
        return appointment_details.appointment.patient


@admin.register(AppointmentSpecialization)
class AppointmentSpecializationAdmin(admin.ModelAdmin):
    list_display = ("appointment", "doctor_name", "patient_name", "specialization", "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('appointment__doctor__first_name',
                     'appointment__patient__first_name', "specialization__name")

    def doctor_name(self, appointment_details):
        return appointment_details.appointment.doctor

    def patient_name(self, appointment_details):
        return appointment_details.appointment.patient


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('question__title',)


@admin.register(DiseaseAnswer)
class DiseaseAnswerAdmin(admin.ModelAdmin):
    list_display = ('value', 'disease', 'questionResponse',
                    "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('value',)


@admin.register(AppointmentFile)
class AppointmentFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'appointment', 'doctor',
                    "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('name',)


class UploadXmlFileForm(forms.Form):
    file_name = forms.CharField(max_length=50)
    xml_file = forms.FileField(
        label='Select a file',
    )


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('name',)
    change_list_template = "admin/appointment/decisiontree/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-xml/', self.upload_xml), ]
        return new_urls + urls

    def parse_xml(self, xml_file, xml, base, q, o, parent_question=None):
        base += q
        if xml.findall(base):
            for question in xml.findall(base):
                is_conditional_question = True if question.get(
                    "isConditionalQuestion") == "true" else False
                default_display = True if question.get(
                    "defaultDisplay") == "true" else False
                survey_question_instance = SurveysQuestion.objects.create(
                    parent_question=parent_question,
                    xml_question_id=int(question.attrib["id"]),
                    question_type=question.get("elementType"),
                    serial_no=int(question.get("serialNo")),
                    title=question.attrib["name"],
                    survey=xml_file,
                    is_conditional_question=is_conditional_question,
                    default_display=default_display,
                )

                if question.findall("./"):
                    for option in question.findall("./"):
                        survey_question_response_instance = SurveyQuestionResponse.objects.create(
                            survey_question=survey_question_instance,
                            xml_question_id=survey_question_instance.xml_question_id,
                            xml_question_response_id=option.attrib["id"],
                            question_response=option.attrib["name"],
                        )

                        if option.find("./"):
                            pass
                        try:
                            if option.findall("./"):
                                survey_answer_target_survey_list = [
                                    SurveyQuestionRelation(
                                        survey_question=survey_question_instance,
                                        question_response=survey_question_response_instance,
                                        xml_parent_question_id=survey_question_instance.xml_question_id,
                                        xml_question_response_id=survey_question_response_instance.xml_question_response_id,
                                        xml_question_response_target_question_id=int(
                                            answer_target.attrib["id"]),
                                    ) for answer_target in option.findall("./")
                                ]
                                SurveyQuestionRelation.objects.bulk_create(
                                    survey_answer_target_survey_list)
                        except:
                            pass

            base += o
            self.parse_xml(xml_file, xml, base, q, o, survey_question_instance)
        else:
            return

    def upload_xml(self, request):
        if request.method == 'POST':
            file_name = request.POST.get("file_name")
            xml_file = request.FILES["xml_file"]
            if not xml_file.name.endswith('.xml'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            xml_file, created = Survey.objects.update_or_create(
                name=file_name,
                file=xml_file
            )
            tree = ET.parse(xml_file.file)
            root = tree.getroot()
            with atomic():
                self.parse_xml(xml_file, root, ".",
                               "/question", "/option", None)

            url = reverse('admin:appointment_survey_changelist')
            return HttpResponseRedirect(url)
        else:
            form = UploadXmlFileForm()
        return render(request, "admin/upload_xml.html", {'form': form})


@admin.register(SurveysQuestion)
class SurveyQuestion(admin.ModelAdmin):
    list_display = ('id', 'parent_question', "xml_question_id", "serial_no", "is_conditional_question", "default_display", 'title', "question_type", 'survey',
                    "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('title',)


@admin.register(SurveyQuestionResponse)
class SurveyQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_question', "xml_question_id", "xml_question_response_id", 'question_response',
                    "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('surveyquestion__title',)

    def survey_id(self, survey_anwser):
        return survey_anwser.survey.id


@admin.register(SurveyQuestionRelation)
class SurveyQuestionRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_question', "question_response", "xml_parent_question_id", "xml_question_response_id", 'xml_question_response_target_question_id',
                    "created_at", "updated_at",)
    search_fields = ('surveyquestion__title',)


admin.site.register(AppointmentSurveyQuestionResponse)
admin.site.register(AppointmentSurvey)
admin.site.register(AppointmentLang)
admin.site.register(AppointmentShortCode)
