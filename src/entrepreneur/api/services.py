from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entrepreneur.models import EntrepreneurForm, Entrepreneur, EntrepreneurImages
from entrepreneur.api.selectors import entrepreneur_form_list, entrepreneur_list, entrepreneur_images_list
from entrepreneur.api.utils import change_all_entrepreneur_form_is_active_field


def entrepreneur_form_create(
    *, title: str,
    is_active: bool = True,
    questions
) -> EntrepreneurForm:
    if is_active == True:
        change_all_entrepreneur_form_is_active_field(True, False)

    entrepreneur_form = EntrepreneurForm.objects.create(title=title, is_active=is_active, questions=questions)
    entrepreneur_form.full_clean()
    entrepreneur_form.save()

    return entrepreneur_form

def entrepreneur_form_update(instance, **data) -> EntrepreneurForm:
    if data.get('is_active') == True:
        change_all_entrepreneur_form_is_active_field(True, False)

    entrepreneur_form = entrepreneur_form_list().filter(pk=instance.pk).update(**data)
    return entrepreneur_form

def entrepreneur_create(
    *, owner,
    project_name: str,
    target_amount: float,
    end_date,
    description: str,
    entrepreneur_form,
    income: float
) -> Entrepreneur:
    entrepreneur = Entrepreneur.objects.create(
        owner=owner, project_name=project_name, target_amount=target_amount, amount_collected=0, end_date=end_date, description=description,
        entrepreneur_form=entrepreneur_form, income=income
    )
    entrepreneur.full_clean()
    entrepreneur.save()

    return entrepreneur

def entrepreneur_update(instance, **data) -> Entrepreneur:
    entrepreneur = entrepreneur_list().filter(pk=instance.pk).update(**data)
    return entrepreneur

def entrepreneur_images_create(
    *,  entrepreneur,
    image: str
) -> EntrepreneurImages:
    entrepreneur_image = EntrepreneurImages.objects.create(entrepreneur=entrepreneur, image=image)
    entrepreneur_image.full_clean()
    entrepreneur_image.save()

    return entrepreneur_image

def entrepreneur_images_update(instance, **data) -> EntrepreneurImages:
    entrepreneur_image = entrepreneur_images_list().filter(pk=instance.pk).update(**data)
    return entrepreneur_image