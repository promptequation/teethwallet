# Generated by Django 3.2.5 on 2022-11-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylang',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Country'),
        ),
    ]
