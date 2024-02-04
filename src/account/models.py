import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField
from micro_investment.validators import compress
from account import enums


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def get_full_name(self) -> str:
        return super().get_full_name()


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="investor")
    birthdate = models.DateField(_("Date of Birth"))
    address = models.CharField(_("Address"), max_length=255)
    marital_status = models.CharField(_("Martial Status"), max_length=50, choices=enums.MartialStatus.choices, default=enums.MartialStatus.SINGLE)
    employment_status = models.CharField(_("Employment Status"), max_length=50, choices=enums.EmploymentStatus.choices, default=enums.EmploymentStatus.WORKING)
    housing_status = models.CharField(_("Housing Status"), max_length=50, choices=enums.HousingStatus.choices, default=enums.HousingStatus.OWN_HOME)
    phone_number = models.CharField(_("Phone number"), max_length=255)
    credit_cart_number = models.CharField(_("Credit Cart Number"), max_length=100)
    debt_amount = models.DecimalField(_("Debt Amount"), max_digits=10, decimal_places=2, default=0)
    monthly_income = models.DecimalField(_("Monthly Income"), max_digits=10, decimal_places=2, default=0)
    references = models.ManyToManyField(User, related_name="investors", verbose_name=_("References"), blank=True)
    profile_picture = models.ImageField(_("Profile Picture"), max_length=1000, upload_to="investor/profile_pictures/", null=True, blank=True,
                                        validators=[FileExtensionValidator(['png',
                                                                            'jpeg',
                                                                            'jpg'])])
    about = models.TextField(_("about"), null=True, blank=True)
    business_activities = models.TextField(_("Business Activities"), null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.profile_picture is not None:
            compressed_profile_pictures = compress(self.profile_picture)
            self.profile_picture = compressed_profile_pictures

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Education(models.Model):
    user = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='education')
    education_place = models.CharField(_("Education Place"), max_length=100)
    education_branch = models.CharField(_("Education Branch"), max_length=100)
    city = models.CharField(_("City"), max_length=255)
    start_year = models.PositiveIntegerField(('Start Year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)],
                                             default=datetime.datetime.now().year)
    end_year = models.PositiveIntegerField(_('End Year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], null=True, blank=True)
    is_continue = models.BooleanField(default=False)


class Experience(models.Model):
    user = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='experience', null=True)
    experience_place = models.CharField(_("Experience Place"), max_length=100)
    position = models.CharField(_("Position"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)
    city = models.CharField(_("City"), max_length=255, null=True, blank=True)
    start_year = models.PositiveIntegerField(('start_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)],
                                             default=datetime.datetime.now().year)
    end_year = models.PositiveIntegerField(('end_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], null=True, blank=True)
    is_continue = models.BooleanField(default=False)


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(_("balance"), max_digits=10, decimal_places=2, default=0)
    money_in_debt_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CompanyBalance(models.Model):
    debt_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    charity_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
