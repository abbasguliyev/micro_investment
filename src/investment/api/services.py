from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from investment.models import Investment
from investment.api.selectors import investment_list

def investment_create(
    *, investor,
    entrepreneur,
    amount: float
) -> Investment:
    if amount <= 0:
        raise ValidationError({"data": _("The amount must be greater than zero!")})
    
    if amount+entrepreneur.amount_collected > entrepreneur.target_amount:
        raise ValidationError({"data": _("The amount you invest is more than the investment target amount")})
    
    
    has_investment = investment_list().filter(investor=investor, entrepreneur=entrepreneur).exists()
    if has_investment:
        raise ValidationError({"data": _("You can invest only 1 time for the same investment")})
    
    investment_income = (entrepreneur.income * amount) / entrepreneur.target_amount
    
    investment = Investment.objects.create(
        investor=investor, entrepreneur=entrepreneur, 
        amount=amount, 
        income=investment_income
    )
    investment.full_clean()
    investment.save()

    entrepreneur.amount_collected = amount
    entrepreneur.save()

    return investment