import datetime

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entrepreneur.models import Entrepreneur, EntrepreneurImages
from entrepreneur.api.selectors import entrepreneur_list, entrepreneur_images_list
from micro_investment.validators import compress
from notification.api.services import notification_create
from account.api.selectors import company_balance_list


def entrepreneur_create(
        *, owner,
        project_name: str,
        start_date,
        end_date,
        description: str,
        count: int = 1,
        purchase_price: float,
        sale_price: float,
        platform_cost_percentage: int = 0,
        investor_share_percentage: int = 0,
        entrepreneur_share_percentage: int = 0,
        debt_to_the_fund_percentage: int = 0,
        charity_to_the_fund_percentage: int = 0

) -> Entrepreneur:
    if owner.user.is_superuser == True or owner.user.is_staff == True:
        is_active = True
    else:
        is_active = False
    total_investment = count * purchase_price
    gross_income = count * sale_price
    platform_cost = (gross_income - total_investment) * int(platform_cost_percentage) / 100
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

    company_balance = company_balance_list().last()
    company_balance.debt_fund = float(company_balance.debt_fund) + float(debt_to_the_fund)
    company_balance.charity_fund = float(company_balance.charity_fund) + float(charity_to_the_fund)
    company_balance.save()

    entrepreneur = Entrepreneur.objects.create(
        owner=owner, project_name=project_name, start_date=start_date, end_date=end_date, description=description,
        count=count, purchase_price=purchase_price, sale_price=sale_price,
        platform_cost_percentage=platform_cost_percentage, investor_share_percentage=investor_share_percentage,
        entrepreneur_share_percentage=entrepreneur_share_percentage, debt_to_the_fund_percentage=debt_to_the_fund_percentage,
        charity_to_the_fund_percentage=charity_to_the_fund_percentage, total_investment=total_investment, gross_income=gross_income,
        platform_cost=platform_cost, final_profit=final_profit, investor_share=investor_share, entrepreneur_share=entrepreneur_share,
        debt_to_the_fund=debt_to_the_fund, charity_to_the_fund=charity_to_the_fund, profit_ratio=profit_ratio, is_active=is_active
    )
    entrepreneur.full_clean()
    entrepreneur.save()

    return entrepreneur


def entrepreneur_update(instance, **data) -> Entrepreneur:
    if data.get("is_finished") is not None and instance.is_finished == False and data.get("is_finished") == True:
        data["finished_date"] = datetime.date.today()
        data["is_active"] = False

        notification_create(user=instance.owner.user, message=f"{instance.project_name} sifarişi yekunlaşdı")
    # if data.get("purchase_price") is None:
    #     purchase_price = instance.purchase_price
    # else:
    #     purchase_price = data.get("purchase_price")

    # if data.get("count") is None:
    #     count = instance.count
    # else:
    #     count = data.get("count")

    # if data.get("sale_price") is None:
    #     sale_price = instance.sale_price
    # else:
    #     sale_price = data.get("sale_price")

    # if data.get("investor_share_percentage") is None:
    #     investor_share_percentage = instance.investor_share_percentage
    # else:
    #     investor_share_percentage = data.get("investor_share_percentage")

    # if data.get("entrepreneur_share_percentage") is None:
    #     entrepreneur_share_percentage = instance.entrepreneur_share_percentage
    # else:
    #     entrepreneur_share_percentage = data.get("entrepreneur_share_percentage")

    # if data.get("debt_to_the_fund_percentage") is None:
    #     debt_to_the_fund_percentage = instance.debt_to_the_fund_percentage
    # else:
    #     debt_to_the_fund_percentage = data.get("debt_to_the_fund_percentage")

    # if data.get("charity_to_the_fund_percentage") is None:
    #     charity_to_the_fund_percentage = instance.charity_to_the_fund_percentage
    # else:
    #     charity_to_the_fund_percentage = data.get("charity_to_the_fund_percentage")

    # total_investment = count * purchase_price
    # gross_income = count * sale_price
    # platform_cost = (gross_income - total_investment) * 2 / 100
    # final_profit = gross_income - total_investment - platform_cost
    # investor_share = final_profit * investor_share_percentage / 100
    # entrepreneur_share = final_profit * entrepreneur_share_percentage / 100
    # debt_to_the_fund = final_profit * debt_to_the_fund_percentage / 100
    # charity_to_the_fund = final_profit * charity_to_the_fund_percentage / 100
    # profit_ratio = (investor_share / total_investment) * 100

    # platform_cost = "%.2f" % platform_cost
    # final_profit = "%.2f" % final_profit
    # investor_share = "%.2f" % investor_share
    # entrepreneur_share = "%.2f" % entrepreneur_share
    # debt_to_the_fund = "%.2f" % debt_to_the_fund
    # charity_to_the_fund = "%.2f" % charity_to_the_fund
    # profit_ratio = float("%.2f" % profit_ratio)

    # if data.get('total_investment') is None:
    #     data["total_investment"] = total_investment
    # else:
    #     data["total_investment"] = instance.total_investment

    # if data.get('gross_income') is None:
    #     data["gross_income"] = gross_income
    # else:
    #     data["gross_income"] = instance.gross_income

    # if data.get('platform_cost') is None:
    #     data["platform_cost"] = platform_cost
    # else:
    #     data["platform_cost"] = instance.platform_cost

    # if data.get('final_profit') is None:
    #     data["final_profit"] = final_profit
    # else:
    #     data["final_profit"] = instance.final_profit

    # if data.get('investor_share') is None:
    #     data["investor_share"] = investor_share
    # else:
    #     data["investor_share"] = instance.investor_share

    # if data.get('entrepreneur_share') is None:
    #     data["entrepreneur_share"] = entrepreneur_share
    # else:
    #     data["entrepreneur_share"] = instance.entrepreneur_share

    # if data.get('debt_to_the_fund') is None:
    #     data["debt_to_the_fund"] = debt_to_the_fund
    # else:
    #     data["debt_to_the_fund"] = instance.debt_to_the_fund

    # if data.get('charity_to_the_fund') is None:
    #     data["charity_to_the_fund"] = charity_to_the_fund
    # else:
    #     data["charity_to_the_fund"] = instance.charity_to_the_fund

    # if data.get('profit_ratio') is None:
    #     data["profit_ratio"] = profit_ratio
    # else:
    #     data["profit_ratio"] = instance.profit_ratio

    if data.get('debt_to_the_fund') is not None:
        company_balance = company_balance_list().last()
        company_balance.debt_fund = float(company_balance.debt_fund) - float(instance.debt_to_the_fund)
        company_balance.save()

        company_balance.debt_fund = float(company_balance.debt_fund) + float(data.get('debt_to_the_fund'))
        company_balance.save()

    print(f"{data=}")

    if data.get('charity_to_the_fund') is not None:
        company_balance = company_balance_list().last()
        company_balance.charity_fund = float(company_balance.charity_fund) - float(instance.charity_to_the_fund)
        company_balance.save()

        company_balance.charity_fund = float(company_balance.charity_fund) + float(data.get('charity_to_the_fund'))
        company_balance.save()

    entrepreneur = entrepreneur_list().filter(pk=instance.pk).update(**data)
    return entrepreneur


def entrepreneur_images_create(
        *, entrepreneur,
        image: str
) -> EntrepreneurImages:
    if image is not None:
        compressed_image = compress(image)
        image = compressed_image

    entrepreneur_image = EntrepreneurImages.objects.create(entrepreneur=entrepreneur, image=image)
    entrepreneur_image.full_clean()
    entrepreneur_image.save()

    return entrepreneur_image


def entrepreneur_images_update(instance, **data) -> EntrepreneurImages:
    entrepreneur_image = entrepreneur_images_list().filter(pk=instance.pk).update(**data)
    return entrepreneur_image
