# Generated by Django 3.2.5 on 2023-01-26 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
