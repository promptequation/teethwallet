from api.models.user_model import MultiLanguage
from .models import *
from import_export.admin import ImportExportModelAdmin
import pandas as pd
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django import forms
from django.shortcuts import render, redirect


@admin.register(Duration)
class DurationAdmin(admin.ModelAdmin):
    list_display = ("number", "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('number',)


@admin.register(Tooth)
class ToothAdmin(admin.ModelAdmin):
    list_display = ("number", "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('number',)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('name',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('name',)


@admin.register(LookUpType)
class LookUpTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('code',)


@admin.register(LookUp)
class LookUpAdmin(admin.ModelAdmin):
    list_display = ("name", 'group', 'code', "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('code',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", 'code', 'state', 'city', 'zipcode', 'country',
                    'is_active', "created_at", "created_by", "updated_by")
    search_fields = ('name',)


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ("company", 'user', 'doctor', 'group', 'status', 'is_owner',
                    'requested_at', 'approval_by', 'approval_at', 'is_active', 'joined_datetime')
    search_fields = ('company',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyUserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['status'].queryset = LookUp.objects.filter(
            group__code="APPROVAL")
        return form


@admin.register(DoctorType)
class DoctorTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'code', "created_at",
                    "updated_at", "created_by", "updated_by")
    search_fields = ('type',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'reference_id', 'element_type', 'is_conditional_question',
                    'serial_no', "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['element_type'].queryset = LookUp.objects.filter(
            group__code="ELEMENT_TYPE")
        return form


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'reference_id', 'serial_no',
                    "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ('title',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', "created_at", "updated_at",
                    "created_by", "updated_by")
    search_fields = ('name',)


class MultiLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_default')


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at",
                    "created_by", "updated_by")
    fieldsets = (
        (None, {
            'fields': ('created_by', 'updated_by')
        }),
    )


class UploadExcelFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
    )


class DiagnosticLangAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'diagnostic', 'lang')
    search_fields = ('name',)
    change_list_template = 'admin/common/diagnosticlang/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-file/', self.upload_excel), ]
        return new_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST':
            form = UploadExcelFileForm(request.POST, request.FILES)
            file = request.FILES['file']
            if not file.name.endswith('.xlsx'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            languages = []
            if file:
                ps = pd.read_excel(file)
                for i in ps.columns:
                    languages.append(MultiLanguage.objects.get(code=i).id)
                for i in range(len(ps)):
                    diagnostic = Diagnostic.objects.create(
                        created_by=request.user,
                        updated_by=request.user,
                    )
                    for j in range(len(languages)):
                        DiagnosticLang.objects.create(
                            name=ps.iloc[i, j], diagnostic=diagnostic, lang=MultiLanguage.objects.get(id=languages[j]))
                    name_list = [f"{MultiLanguage.objects.get(id=languages[j]).code}: {ps.iloc[i, j]}" for j in range(
                        len(languages))]
                    name = " || ".join(tuple(name_list))
                    diagnostic.name = str(name)
                    diagnostic.save()
                messages.success(request, "File uploaded successfully")
            return redirect('admin:common_diagnosticlang_changelist')
        form = UploadExcelFileForm()
        context = {'form': form}
        return render(request, 'admin/common/diagnosticlang/upload_file.html', context)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at",
                    "created_by", "updated_by")
    fieldsets = (
        (None, {
            'fields': ('created_by', 'updated_by')
        }),
    )


class UploadCsvTreatmentFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
    )


class TreatmentLangAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'treatment', 'lang')
    search_fields = ('name',)
    change_list_template = 'admin/common/treatmentlang/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-file/', self.upload_excel), ]
        return new_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST':
            form = UploadCsvTreatmentFileForm(request.POST, request.FILES)
            file = request.FILES['file']
            languages = []
            if file:
                ps = pd.read_excel(file)
                for i in ps.columns:
                    languages.append(MultiLanguage.objects.get(code=i).id)
                for i in range(len(ps)):
                    treatment = Treatment.objects.create(
                        created_by=request.user,
                        updated_by=request.user,
                    )
                    for j in range(len(languages)):
                        TreatmentLang.objects.create(
                            name=ps.iloc[i, j], treatment=treatment, lang=MultiLanguage.objects.get(id=languages[j]))
                    name_list = [f"{MultiLanguage.objects.get(id=languages[j]).code}: {ps.iloc[i, j]}" for j in range(
                        len(languages))]
                    name = " || ".join(tuple(name_list))
                    treatment.name = name
                    treatment.save()
                messages.success(request, "File uploaded successfully")
            return redirect('admin:common_treatmentlang_changelist')
        form = UploadCsvTreatmentFileForm()
        context = {'form': form}
        return render(request, 'admin/common/treatmentlang/upload_file.html', context)


@admin.register(PredefinedAppointmentFollowUpCombination)
class AdminPredefinedAppointmentFollowUpCombination(admin.ModelAdmin):
    change_form_template = 'admin/common/predefinedappointmentfollowupcombination/change_form.html'


admin.site.register(MultiLanguage, MultiLanguageAdmin)
admin.site.register(CompanyLang)
admin.site.register(DiagnosticLang, DiagnosticLangAdmin)
admin.site.register(TreatmentLang, TreatmentLangAdmin)
admin.site.register(SpecializationLang)
admin.site.register(QuestionLang)
admin.site.register(QuestionResponseLang)
admin.site.register(QualificationLang)
admin.site.register(PriorityLang)
admin.site.register(AppointmentCode)
