import django_filters
from investment.models import Investment, InvestmentReport


class InvestmentFilter(django_filters.FilterSet):
    class Meta:
        model = Investment
        fields = {
            'investor': ['exact'],
            'entrepreneur': ['exact'],
            'investment_date': ['exact'],
            'is_submitted': ['exact']
        }


class InvestmentReportFilter(django_filters.FilterSet):
    entrepreneur = django_filters.CharFilter(method="entrepreneur_filter", label="entrepreneur")

    def entrepreneur_filter(self, queryset, name, value):
        qs = queryset.filter(investment__entrepreneur=value)
        return qs

    class Meta:
        model = InvestmentReport
        fields = {
            'investor': ['exact'],
            'investment': ['exact'],
        }
