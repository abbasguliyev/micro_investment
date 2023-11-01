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
    
    if amount+entrepreneur.amount_collected > entrepreneur.total_investment:
        raise ValidationError({"data": _("The amount you invest is more than the total investment amount")})
    
    has_investment = investment_list().filter(investor=investor, entrepreneur=entrepreneur).exists()
    if has_investment:
        raise ValidationError({"data": _("You can invest only 1 time for the same investment")})
    
    profit = amount * entrepreneur.profit_ratio / 100
    
    investment = Investment.objects.create(
        investor=investor, entrepreneur=entrepreneur, 
        amount=amount, 
        profit=profit
    )
    investment.full_clean()
    investment.save()

    entrepreneur.amount_collected = amount
    entrepreneur.save()

    return investment