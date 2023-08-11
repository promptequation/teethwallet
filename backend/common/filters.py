from django_filters import FilterSet, CharFilter
from .models import Company, CompanyUser, AppointmentCode


class CompanyFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    state = CharFilter(lookup_expr='icontains')
    zipcode = CharFilter(lookup_expr='icontains')
    country = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = ['id', 'name', 'state', 'city', 'zipcode',
                  'country', 'is_active', 'created_by__id', 'updated_by__id']


class CompanyUserFilter(FilterSet):
    user__first_name = CharFilter(lookup_expr='icontains')
    user__last_name = CharFilter(lookup_expr='icontains')
    user__name = CharFilter(lookup_expr='icontains')
    user__username = CharFilter(lookup_expr='icontains')
    user__email = CharFilter(lookup_expr='icontains')
    company__name = CharFilter(lookup_expr='icontains')
    group__name = CharFilter(lookup_expr='icontains')
    status__name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = CompanyUser
        fields = ["id", "user__id", "company__id", "group__id", "group__name", "status__id", "doctor__id",
                  "requested_at", "requested_by__id", "approval_by__id", "is_owner", "is_active"]


class AppointmentCodeFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    code = CharFilter(field_name="code", lookup_expr='icontains')
    description = CharFilter(field_name="description", lookup_expr='icontains')
    lang = CharFilter(field_name="lang__id", lookup_expr='exact')

    class Meta:
        model = AppointmentCode
        fields = "__all__"
