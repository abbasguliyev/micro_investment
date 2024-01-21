from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
import django_filters
from account.models import Investor, Experience, Education


class InvestorFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(method="fullname_filter", label="fullname")
    is_active = django_filters.BooleanFilter(method="is_active_filter", label="is_active")

    def fullname_filter(self, queryset, name, value):
        qs = queryset.annotate(fullname=Concat('user__first_name', V(' '), 'user__last_name')).filter(fullname__icontains=value)
        return qs

    def is_active_filter(self, queryset, name, value):
        qs = queryset.filter(user__is_active=value)
        return qs

    class Meta:
        model = Investor
        fields = {
            'birthdate': ['exact'],
            'marital_status': ['exact'],
            'employment_status': ['exact'],
            'housing_status': ['exact'],
            'phone_number': ['exact'],
            'monthly_income': ['exact', 'gte', 'lte']
        }


class ExperienceFilter(django_filters.FilterSet):
    class Meta:
        model = Experience
        fields = {
            'user': ['exact'],
            'experience_place': ['exact', 'icontains'],
            'position': ['exact', 'icontains'],
            'city': ['exact', 'icontains'],
            'start_year': ['exact', 'gte', 'lte'],
            'end_year': ['exact', 'gte', 'lte'],
            'is_continue': ['exact']
        }


class EducationFilter(django_filters.FilterSet):
    class Meta:
        model = Education
        fields = {
            'user': ['exact'],
            'education_place': ['exact', 'icontains'],
            'education_branch': ['exact', 'icontains'],
            'city': ['exact', 'icontains'],
            'start_year': ['exact', 'gte', 'lte'],
            'end_year': ['exact', 'gte', 'lte'],
            'is_continue': ['exact']
        }
