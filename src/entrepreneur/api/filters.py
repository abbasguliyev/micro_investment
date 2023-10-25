import django_filters
from entrepreneur.models import Entrepreneur, EntrepreneurForm, EntrepreneurImages

class EntrepreneurFilter(django_filters.FilterSet):
    class Meta:
        model = Entrepreneur
        fields = {
            'owner': ['exact'],
            'project_name': ['exact', 'icontains'],
            'target_amount': ['exact', 'gte', 'lte'],
            'amount_collected': ['exact', 'gte', 'lte'],
            'start_date': ['exact', 'gte', 'lte'],
            'end_date': ['exact', 'gte', 'lte'],
            'entrepreneur_form': ['exact'],
            'is_active': ['exact'],
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

