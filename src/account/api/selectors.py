from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from account.models import Education, Experience, Investor, UserBalance


def user_list() -> QuerySet[get_user_model()]:
    qs = get_user_model().objects.prefetch_related('user_permissions', 'groups').all()
    return qs

def investor_list() -> QuerySet[Investor]:
    qs = Investor.objects.select_related('user').prefetch_related('references').all()
    return qs

def experience_list() -> QuerySet[Experience]:
    qs = Experience.objects.select_related('user').all()
    return qs

def education_list() -> QuerySet[Education]:
    qs = Education.objects.select_related('user').all()
    return qs

def user_balance_list() -> QuerySet[UserBalance]:
    qs = UserBalance.objects.select_related('user').all()
    return qs