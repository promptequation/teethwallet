import datetime
from api.enums.nationality_enum import NationalityEnum
from api.models.base_model import BaseModel
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from utilities.fixed_values import GENDER_CHOICES
from versatileimagefield.fields import VersatileImageField


class User(AbstractUser, BaseModel):
    first_name = models.CharField(
        _('First name'), null=True, blank=True, max_length=150)
    last_name = models.CharField(
        _('Last name'), null=True, blank=True, max_length=150)
    name = models.CharField(_('Name'), null=True, blank=True, max_length=150)
    username = models.CharField(
        _('Username'), null=True, blank=True, unique=True, max_length=30)
    email = models.EmailField(_('Email'), null=True,
                              blank=True, unique=True, max_length=50)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(_('Phone'), null=True,
                             blank=True, unique=True, max_length=10)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    avatar = VersatileImageField(
        upload_to="media/user-avatars", blank=True, null=True)
    street = models.CharField(
        _('Street'), max_length=150, blank=True, null=True)
    street2 = models.CharField(
        _('Street 2'), max_length=150, blank=True, null=True)
    state = models.CharField(_('State'), max_length=150, blank=True, null=True)
    city = models.CharField(_('City'), max_length=150, blank=True, null=True)
    zip = models.CharField(_('Zip'), max_length=255, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    nationality = models.SmallIntegerField(
        choices=[(_nationality.value, _nationality.name) for _nationality in NationalityEnum], null=True, blank=True)
    language_code = models.CharField(
        max_length=35, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, null=True, blank=True)
    lang = models.ForeignKey(
        "MultiLanguage", on_delete=models.CASCADE, null=True, blank=True)
    is_caregiver = models.BooleanField(default=False, blank=True, null=True)
    access_survey = models.BooleanField(default=False, blank=True, null=True)
    is_first_login = models.BooleanField(default=True, blank=True, null=True)
    end_login_date = models.DateTimeField(null=True, blank=True)
    counter = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'api'

    def __str__(self):
        return str(self.username)

    def user_age(self, dob: object = None):
        today = datetime.date.today()
        age = relativedelta(today, dob)
        return age.years

    def save(self, *args, **kwargs):
        if self.user_age(dob=self.date_of_birth) < 18:
            self.is_caregiver = True
        else:
            self.is_caregiver = False
        return super(User, self).save()


class MultiLanguage(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    is_default = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class UserLang(models.Model):
    lang = models.ForeignKey(
        MultiLanguage, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(
        _('First name'), null=True, blank=True, max_length=150)
    last_name = models.CharField(
        _('Last name'), null=True, blank=True, max_length=150)
    name = models.CharField(_('Name'), null=True, blank=True, max_length=150)
    gender = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(_('Phone'), null=True,
                             blank=True, unique=True, max_length=10)
    street = models.CharField(
        _('Street'), max_length=150, blank=True, null=True)
    street2 = models.CharField(
        _('Street 2'), max_length=150, blank=True, null=True)
    state = models.CharField(_('State'), max_length=150, blank=True, null=True)
    city = models.CharField(_('City'), max_length=150, blank=True, null=True)
    zip = models.CharField(_('Zip'), max_length=255, blank=True, null=True)
