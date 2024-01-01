from django.utils.translation import gettext_lazy as _
from django.db import models


class Investment(models.Model):
    investor = models.ForeignKey('account.Investor', on_delete=models.CASCADE, related_name="investments")
    entrepreneur = models.ForeignKey('entrepreneur.Entrepreneur', on_delete=models.CASCADE, related_name="investments")
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    amount_must_send = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_deducated_from_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(_('Profit'), max_digits=10, decimal_places=2)
    final_profit = models.DecimalField(_('Final Profit'), max_digits=10, decimal_places=2)
    investment_date = models.DateField(_("Investment date"), auto_now_add=True, help_text="Yatırım tarixi")
    is_submitted = models.BooleanField(default=False)
    is_amount_sended = models.BooleanField(default=False)
    is_amount_sended_submitted = models.BooleanField(default=False)
    is_from_debt_fund = models.BooleanField(default=False)
    amount_from_debt_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('investor__user__first_name',)


class InvestmentReport(models.Model):
    investor = models.ForeignKey('account.Investor', on_delete=models.CASCADE, related_name="investment_report")
    investment = models.ForeignKey('investment.Investment', on_delete=models.CASCADE, related_name="investment_report")
    amount_want_to_send_to_cart = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_want_to_keep_in_the_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_want_to_send_to_charity_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_want_to_send_to_debt_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)
    is_amount_sended_to_investor = models.BooleanField(default=False)

    class Meta:
        ordering = ('investor__user__first_name',)
