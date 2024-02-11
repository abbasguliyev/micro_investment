import django_filters
from investment.models import Investment, InvestmentReport
from django.db.models.functions import Concat   
from django.db.models import Value as V

class InvestmentFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(method="fullname_filter", label="fullname")

    def fullname_filter(self, queryset, name, value):
        qs = queryset.annotate(fullname=Concat('investor__user__first_name', V(' '), 'investor__user__last_name')).filter(fullname__icontains=value)
        return qs

    class Meta:
        model = Investment
        fields = {
            'investor': ['exact'],
            'entrepreneur': ['exact'],
            'entrepreneur__project_name': ['icontains'],
            'entrepreneur__is_finished': ['exact'],
            'investment_date': ['exact'],
            'is_submitted': ['exact'],
            'is_amount_sended': ['exact'],
            'is_amount_sended_submitted': ['exact'],
            'amount_must_send': ['exact', 'gt'],
            'is_from_debt_fund': ['exact']
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
