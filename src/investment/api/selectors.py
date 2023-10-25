from django.db.models.query import QuerySet
from investment.models import Investment

def investment_list() -> QuerySet[Investment]:
    qs = Investment.objects.select_related('investor', 'entrepreneur').all()
    return qs
