from django.db.models.query import QuerySet
from investment.models import Investment, InvestmentReport

def investment_list() -> QuerySet[Investment]:
    qs = Investment.objects.select_related('investor', 'entrepreneur').order_by("-pk").all()
    return qs

def investment_report_list() -> QuerySet[Investment]:
    qs = InvestmentReport.objects.select_related('investor', 'investment').order_by("-pk").all()
    return qs
