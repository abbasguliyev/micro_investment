import django_filters
from investment.models import Investment

class InvestmentFilter(django_filters.FilterSet):
    class Meta:
        model = Investment
        fields = {
            'investor': ['exact'],
            'entrepreneur': ['exact'],
            'amount': ['exact', 'gte', 'lte']
        }