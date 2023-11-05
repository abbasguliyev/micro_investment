import django_filters
from entrepreneur.models import Entrepreneur, EntrepreneurForm, EntrepreneurImages

class EntrepreneurFilter(django_filters.FilterSet):
    class Meta:
        model = Entrepreneur
        fields = {
            'owner': ['exact'],
            'start_date': ['exact', 'gte', 'lte'],
            'end_date': ['exact', 'gte', 'lte']
        }

class EntrepreneurFormFilter(django_filters.FilterSet):
    class Meta:
        model = EntrepreneurForm
        fields = {
            'title': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class EntrepreneurImagesFilter(django_filters.FilterSet):
    class Meta:
        model = EntrepreneurImages
        fields = {
            'entrepreneur': ['exact']
        }

