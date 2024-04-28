from django.db.models.query import QuerySet
from investment.models import Investment, InvestmentReport


def investment_list() -> QuerySet[Investment]:
    qs = Investment.objects.select_related('investor', 'entrepreneur').order_by("entrepreneur__project_name", "pk").all()
    return qs


def investment_report_list() -> QuerySet[InvestmentReport]:
    qs = InvestmentReport.objects.select_related('investor', 'investment').order_by("investor__user__first_name").all()
    return qs


def admin_investment_list() -> QuerySet[Investment]:
    qs = Investment.objects.select_related('investor', 'entrepreneur').order_by("investor__user__first_name", "pk").all()
    return qs
