from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from micro_investment.validators import compress

class EntrepreneurForm(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    questions = models.JSONField()

class Entrepreneur(models.Model):
    owner = models.ForeignKey("account.Investor", on_delete=models.CASCADE, related_name="entrepreneurs")
    project_name = models.CharField(_("Project name"), max_length=255)
    target_amount = models.DecimalField(_("Target amount"), max_digits=10, decimal_places=2)
    amount_collected = models.DecimalField(_("Amount collected"), max_digits=10, decimal_places=2)
    start_date = models.DateField(_("Start date"), auto_now_add=True)
    end_date = models.DateField(_("End date"))
    description = models.TextField()
    entrepreneur_form = models.ForeignKey(EntrepreneurForm, on_delete=models.SET_NULL, related_name="entrepreneurs", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    income = models.FloatField(default=0)

class EntrepreneurImages(models.Model):
    entrepreneur = models.ForeignKey(Entrepreneur, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("Entrepreneur Image"), upload_to="investor/entrepreneur_image/", validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])

    def save(self, *args, **kwargs) -> None:
        if self.image is not None:
            compressed_image = compress(self.image)
            self.image = compressed_image

        super().save(*args, **kwargs)