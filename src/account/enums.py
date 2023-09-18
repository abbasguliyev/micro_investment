from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class MartialStatus(TextChoices):
    SINGLE = "single", _("Single")
    MARRIED = "married", _("Married")


class EmploymentStatus(TextChoices):
    WORKING = "working", _("Working")
    UNEMPLOYED = "unemployed", _("Unemployed")


class HousingStatus(TextChoices):
    RENTING = "renting", _("Renting")
    OWN_HOME = "own home", _("Own Home")