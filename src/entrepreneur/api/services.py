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
    end_date,
    description: str,
    entrepreneur_form,
    count: int = 1,
    purchase_price: float,
    sale_price: float,
    platform_cost_percentage: int = 0,
    investor_share_percentage: int = 0,
    entrepreneur_share_percentage: int = 0,
    debt_to_the_fund_percentage: int = 0,
    charity_to_the_fund_percentage: int = 0
    
) -> Entrepreneur:
    total_investment = count * purchase_price
    gross_income = count * sale_price
    platform_cost = (gross_income - total_investment) * 2 / 100
    final_profit = gross_income - total_investment - platform_cost
    investor_share = final_profit * investor_share_percentage / 100
    entrepreneur_share = final_profit * entrepreneur_share_percentage / 100
    debt_to_the_fund = final_profit * debt_to_the_fund_percentage / 100
    charity_to_the_fund = final_profit * charity_to_the_fund_percentage / 100
    profit_ratio = (investor_share / total_investment) * 100

    platform_cost = "%.2f" % platform_cost
    final_profit = "%.2f" % final_profit
    investor_share = "%.2f" % investor_share
    entrepreneur_share = "%.2f" % entrepreneur_share
    debt_to_the_fund = "%.2f" % debt_to_the_fund
    charity_to_the_fund = "%.2f" % charity_to_the_fund
    profit_ratio = float("%.2f" % profit_ratio)

    entrepreneur = Entrepreneur.objects.create(
        owner=owner, project_name=project_name, end_date=end_date, description=description,
        entrepreneur_form=entrepreneur_form, count=count, purchase_price=purchase_price, sale_price=sale_price,
        platform_cost_percentage=platform_cost_percentage, investor_share_percentage=investor_share_percentage,
        entrepreneur_share_percentage=entrepreneur_share_percentage, debt_to_the_fund_percentage=debt_to_the_fund_percentage,
        charity_to_the_fund_percentage=charity_to_the_fund_percentage, total_investment=total_investment, gross_income=gross_income,
        platform_cost=platform_cost, final_profit=final_profit, investor_share=investor_share, entrepreneur_share=entrepreneur_share,
        debt_to_the_fund=debt_to_the_fund, charity_to_the_fund=charity_to_the_fund, profit_ratio=profit_ratio
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