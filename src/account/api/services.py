import datetime

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from account.models import Investor, Experience, Education, UserBalance
from account.api.selectors import user_list, investor_list, experience_list, education_list


def user_create(
        *, first_name: str,
        last_name: str,
        email: str,
        password: str
) -> get_user_model():
    user = get_user_model().objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
    return user


def user_update(instance, **data) -> get_user_model():
    user = user_list().filter(pk=instance.pk).update(**data)
    return user


def investor_create(
        *, first_name: str,
        last_name: str,
        email: str,
        password: str,
        birthdate: datetime.date,
        address: str,
        marital_status: str,
        employment_status: str,
        housing_status: str,
        phone_number: str,
        credit_cart_number: str,
        debt_amount: float = 0,
        monthly_income: float = 0,
        references=[],
        profile_picture=None,
        about: str = None,
        business_activities: str = None
) -> Investor:
    user_exists = user_list().filter(email=email).exists()
    if user_exists:
        raise ValidationError({"detail": _("Zəhmət olmasa doğru emaili daxil etdiyinizdən əmin olun")})

    user = user_create(first_name=first_name, last_name=last_name, email=email, password=password)
    check_investor_instance_of_user = investor_list().filter(user=user)
    if check_investor_instance_of_user.count() == 0:
        investor = Investor.objects.create(
            user=user, birthdate=birthdate, address=address,
            marital_status=marital_status, employment_status=employment_status,
            housing_status=housing_status, phone_number=phone_number,
            credit_cart_number=credit_cart_number, debt_amount=debt_amount,
            monthly_income=monthly_income, profile_picture=profile_picture, about=about,
            business_activities=business_activities
        )
        investor.full_clean()
        investor.save()
    else:
        investor = check_investor_instance_of_user.update(
            user=user, birthdate=birthdate, address=address,
            marital_status=marital_status, employment_status=employment_status,
            housing_status=housing_status, phone_number=phone_number,
            credit_cart_number=credit_cart_number, debt_amount=debt_amount,
            monthly_income=monthly_income, profile_pictures=profile_picture, about=about,
            business_activities=business_activities
        )

    if references is not None:
        investor.references.set(references.split(","))
        investor.save

    return investor


def investor_update(instance, **data) -> Investor:
    user_data = dict()
    if data.get("first_name") is not None:
        user_data["first_name"] = data.pop("first_name")
    if data.get("last_name") is not None:
        user_data["last_name"] = data.pop("last_name")
    if data.get("email") is not None:
        user_data["email"] = data.pop("email")

    user = user_list().filter(investor=instance).update(**user_data)
    investor = investor_list().filter(pk=instance.pk).update(**data)
    return investor


def education_create(
        *, user,
        education_place: str,
        education_branch: str,
        city: str,
        start_year: int = datetime.datetime.now().year,
        end_year: int = None,
        is_continue: bool = False
) -> Education:
    if is_continue == False and end_year is not None and end_year <= start_year:
        raise ValidationError({"detail": _("Bitmə ili başlanğıc ilindən əvvəl ola bilməz")})

    if is_continue == False and end_year is None:
        raise ValidationError({"detail": _("Bitmə tarixini daxil edin")})

    if is_continue == True and end_year is not None:
        end_year = None

    education = Education.objects.create(
        user=user, education_place=education_place, education_branch=education_branch,
        city=city, start_year=start_year, end_year=end_year, is_continue=is_continue
    )
    education.full_clean()
    education.save()

    return education


def education_update(instance, **data) -> Education:
    education = education_list().filter(pk=instance.pk).update(**data)
    return education


def experience_create(
        *, user,
        experience_place: str,
        position: str,
        description: str = None,
        city: str,
        start_year: int = datetime.datetime.now().year,
        end_year: int = None,
        is_continue: bool = False
) -> Experience:
    if is_continue == False and end_year is not None and end_year <= start_year:
        raise ValidationError({"detail": _("Bitmə ili başlanğıc ilindən əvvəl ola bilməz")})

    if is_continue == False and end_year is None:
        raise ValidationError({"detail": _("Bitmə tarixini daxil edin")})

    if is_continue == True and end_year is not None:
        end_year = None

    experience = Experience.objects.create(
        user=user, experience_place=experience_place, position=position, description=description,
        city=city, start_year=start_year, end_year=end_year, is_continue=is_continue
    )
    experience.full_clean()
    experience.save()

    return experience


def experience_update(instance, **data) -> Experience:
    experience = experience_list().filter(pk=instance.pk).update(**data)
    return experience


def user_balance_create(*, user, balance: float = 0) -> UserBalance:
    user_balance = UserBalance.objects.create(user=user, balance=balance)
    user_balance.full_clean()
    user_balance.save()

    return user_balance