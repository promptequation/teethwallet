# Generated by Django 3.2.5 on 2023-01-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='if_active',
            field=models.BooleanField(default=True),
        ),
    ]
