from django.utils.translation import gettext_lazy as _
from django.db import models


class Investment(models.Model):
    investor = models.ForeignKey('account.Investor', on_delete=models.CASCADE, related_name="investments")
    entrepreneur = models.ForeignKey('entrepreneur.Entrepreneur', on_delete=models.CASCADE, related_name="investments")
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    profit = models.DecimalField(_('Profit'), max_digits=10, decimal_places=2)
    investment_date = models.DateField(_("Investment date"), auto_now_add=True, help_text="Yatırım tarixi")