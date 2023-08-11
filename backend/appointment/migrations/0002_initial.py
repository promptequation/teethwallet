# Generated by Django 3.2.5 on 2022-10-31 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('appointment', '0001_initial'),
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='diseaseanswer',
            name='questionResponse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.questionresponse'),
        ),
        migrations.AddField(
            model_name='diseaseanswer',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disease_answer_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='disease',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disease_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='disease',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.question'),
        ),
        migrations.AddField(
            model_name='disease',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disease_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='disease',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentsurveyquestionresponse',
            name='appointment_survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointmentsurvey'),
        ),
        migrations.AddField(
            model_name='appointmentsurveyquestionresponse',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_survey_question_response_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentsurveyquestionresponse',
            name='question_response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.surveyquestionresponse'),
        ),
        migrations.AddField(
            model_name='appointmentsurveyquestionresponse',
            name='survey_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.surveysquestion'),
        ),
        migrations.AddField(
            model_name='appointmentsurveyquestionresponse',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_survey_question_response_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentsurvey',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_survey', to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentsurvey',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_survey_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentsurvey',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.survey'),
        ),
        migrations.AddField(
            model_name='appointmentsurvey',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_survey_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentspecialization',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentspecialization',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_specialization_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentspecialization',
            name='specialization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.specialization'),
        ),
        migrations.AddField(
            model_name='appointmentspecialization',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_specialization_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentshortcode',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentshortcode',
            name='appointment_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.appointmentcode'),
        ),
        migrations.AddField(
            model_name='appointmentshortcode',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_short_code_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentshortcode',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_short_code_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentpriority',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentpriority',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_type_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentpriority',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.priority'),
        ),
        migrations.AddField(
            model_name='appointmentpriority',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_type_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentlang',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentlang',
            name='lang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.multilanguage'),
        ),
        migrations.AddField(
            model_name='appointmentfile',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentfile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointmentFile_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentfile',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointmentFile_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentfile',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointmentFile_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_details', to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_details_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='diagnosis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_diagnostic', to='common.diagnostic'),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='tooth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_tooth', to='common.tooth'),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='treatment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_treatment', to='common.treatment'),
        ),
        migrations.AddField(
            model_name='appointmentdetail',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_details_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_doctor_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
