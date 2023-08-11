from django.contrib import admin
from .models import UserQualification, UserSpecialization


@admin.register(UserQualification)
class UserQualificationAdmin(admin.ModelAdmin):
    list_display = ("user", "qualification")
    search_fields = ('user',)


@admin.register(UserSpecialization)
class UserSpecializationAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization")
    search_fields = ('user',)
