import django_filters
from entrepreneur.models import Entrepreneur, EntrepreneurImages


class EntrepreneurFilter(django_filters.FilterSet):
    class Meta:
        model = Entrepreneur
        fields = {
            'owner': ['exact'],
            'project_name': ['exact', 'icontains'],
            'start_date': ['exact', 'gte', 'lte'],
            'end_date': ['exact', 'gte', 'lte'],
            'is_active': ['exact'],
            'is_finished': ['exact']
        }


class EntrepreneurImagesFilter(django_filters.FilterSet):
    class Meta:
        model = EntrepreneurImages
        fields = {
            'entrepreneur': ['exact']
        }
