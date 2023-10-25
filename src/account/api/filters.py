import django_filters
from account.models import Investor, Experience, Education

class InvestorFilter(django_filters.FilterSet):
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

