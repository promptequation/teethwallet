from django.shortcuts import render, HttpResponse
from .models import *
import csv


def csv_view(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Patient Name', 'Appointment ID', 'Date', 'Doctor Name',
                    'Company Name', 'Survey', 'Questions', 'Answers'])
    for value in AppointmentSurveyQuestionResponse.objects.filter(appointment_survey__survey_id=survey_id).values_list(
        'appointment_survey__appointment__patient__name',
        'appointment_survey__appointment__id',
        'created_at',
        'appointment_survey__appointment__doctor__name',
        'appointment_survey__appointment__company__name',
        'appointment_survey__survey__name', 'survey_question__title',
        'response_value'
    ):
        writer.writerow(value)
    name = survey.name
    response['Content-Disposition'] = f'attachment; filename = "{name}.csv"'
    return response


def download_csv(request):
    survey = Survey.objects.all()
    contex = {
        'survey': survey
    }
    return render(request, 'SurveyList.html', contex)
