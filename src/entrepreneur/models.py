import django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from micro_investment.validators import compress

class Entrepreneur(models.Model):
    owner = models.ForeignKey("account.Investor", on_delete=models.CASCADE, related_name="entrepreneurs", help_text="Formaçı")
    project_name = models.CharField(_("Project name"), max_length=255, help_text="Proyekt adı")
    start_date = models.DateField(_("Start date"), default=django.utils.timezone.now, help_text="Başlanğıc tarixi")
    end_date = models.DateField(_("End date"), help_text="Bitmə tarixi")
    finished_date = models.DateField(_("Finished date"), null=True, blank=True, help_text="Yekunlaşdığı tarix")
    description = models.TextField(help_text="Açıqlama")
    is_active = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    count = models.IntegerField(default=1, blank=True)

    purchase_price = models.DecimalField(_("Purchase price"), max_digits=10, decimal_places=2, default=0, help_text="Alış qiyməti")
    sale_price = models.DecimalField(_("Sale price"), max_digits=10, decimal_places=2, default=0, help_text="Satış qiyməti")

    total_investment = models.DecimalField(_("Total Investment"), max_digits=10, decimal_places=2, default=0, help_text="Ümumi investisiya")
    gross_income = models.DecimalField(_("Gross income"), max_digits=10, decimal_places=2, default=0, help_text="Ümumi gəlir")

    platform_cost_percentage = models.PositiveIntegerField(_("Platform cost percentage"), default=2, help_text="Platforma xərci faizi")
    platform_cost = models.DecimalField(_("Platform cost"), max_digits=10, decimal_places=2, default=0, help_text="Platforma xərci")

    final_profit = models.DecimalField(_("Final profit"), max_digits=10, decimal_places=2, default=0, help_text="Yekun Mənfəət")

    investor_share_percentage = models.PositiveIntegerField(_("Investor share percentage"), default=30, help_text="İnvestorun payı faizi")
    investor_share = models.DecimalField(_("Investor share"), max_digits=10, decimal_places=2, default=0, help_text="İnvestorun payı")

    entrepreneur_share_percentage = models.PositiveIntegerField(_("Entrepreneur share percentage"), default=65, help_text="Formaçının payı faizi")
    entrepreneur_share = models.DecimalField(_("Entrepreneur share"), max_digits=10, decimal_places=2, default=0, help_text="Formaçının payı")

    debt_to_the_fund_percentage = models.PositiveIntegerField(_("Debt to the fund percentage"), default=5, help_text="Fonda borc faizi")
    debt_to_the_fund = models.DecimalField(_("Debt to the fund"), max_digits=10, decimal_places=2, default=0, help_text="Fonda borc")

    charity_to_the_fund_percentage = models.PositiveIntegerField(_("Charity to the fund percentage"), default=0, help_text="Fonda sədəqə faizi")
    charity_to_the_fund = models.DecimalField(_("Charity to the fund"), max_digits=10, decimal_places=2, default=0, help_text="Fonda sədəqə")

    profit_ratio = models.FloatField(_("Profit ratio"), default=0, help_text="Mənfəət əmsalı")

    amount_collected = models.DecimalField(_("Amount collected"), max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.project_name


class EntrepreneurImages(models.Model):
    entrepreneur = models.ForeignKey(Entrepreneur, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("Entrepreneur Image"), max_length=1000, upload_to="investor/entrepreneur_image/", validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])