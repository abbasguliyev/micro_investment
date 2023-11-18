from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from investment.models import Investment
from investment.api.selectors import investment_list

def investment_create(
    *, request_user, investor,
    entrepreneur,
    amount: float,
    is_submitted: bool = False
) -> Investment:
    if amount <= 0:
        raise ValidationError({"detail": _("The amount must be greater than zero!")})
    
    if amount+entrepreneur.amount_collected > entrepreneur.total_investment:
        raise ValidationError({"detail": _("The amount you invest is more than the total investment amount")})
    
    has_investment = investment_list().filter(investor=investor, entrepreneur=entrepreneur).exists()
    if has_investment:
        raise ValidationError({"detail": _("You can invest only 1 time for the same investment")})
    
    if investor is None:
        investor = request_user
    
    profit = float(amount) * float(entrepreneur.profit_ratio) / 100
    final_profit=float(amount)+float(profit)
    
    investment = Investment.objects.create(
        investor=investor, entrepreneur=entrepreneur, 
        amount=amount, 
        profit=profit,
        final_profit=final_profit,
        is_submitted=is_submitted
    )
    investment.full_clean()
    investment.save()

    entrepreneur.amount_collected = entrepreneur.amount_collected + amount
    entrepreneur.save()

    return investment

def investment_update(instance, **data) -> Investment:
    investment = investment_list().filter(pk=instance.pk).update(**data)
    return investment