from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from investment.models import Investment, InvestmentReport
from investment.api.selectors import investment_list, investment_report_list
from account.api.selectors import company_balance_list, user_balance_list
from account.api.services import company_balance_create
from notification.api.services import notification_create
import logging

logger = logging.getLogger(__name__)


def investment_create(
        *, request_user, investor,
        entrepreneur,
        amount: float,
        is_submitted: bool = False,
        is_from_debt_fund: bool = False,
        amount_from_debt_fund: float = 0
) -> Investment:
    if amount <= 0:
        raise ValidationError({"detail": _("Məbləğ 0-dan böyük olmalıdır!")})

    if amount + entrepreneur.amount_collected > entrepreneur.total_investment:
        raise ValidationError({"detail": _("Məbləğ sifarişin yekun toplanmış məbləğindən çox ola bilməz")})

    has_investment = investment_list().filter(investor=investor, entrepreneur=entrepreneur).exists()
    if has_investment:
        raise ValidationError({"detail": _("Eyni sifarişə yalnız 1 dəfə yatırım edə bilərsiniz")})

    if is_from_debt_fund == True:
        if float(amount_from_debt_fund) > float(amount):
            raise ValidationError({"detail": _("Borc fondundan qarşılanacaq məbləğ yekun məbləğdən çox ola bilməz")})

    if is_from_debt_fund == False:
        amount_from_debt_fund = 0

    if investor is None:
        investor = request_user

    profit = float(amount) * float(entrepreneur.profit_ratio) / 100
    profit = "{:.2f}".format(profit)
    final_profit = float(amount) + float(profit)
    final_profit = "{:.2f}".format(final_profit)

    investment = Investment.objects.create(
        investor=investor,
        entrepreneur=entrepreneur,
        amount=amount,
        profit=profit,
        final_profit=final_profit,
        is_submitted=is_submitted,
        is_from_debt_fund=is_from_debt_fund,
        amount_from_debt_fund=amount_from_debt_fund
    )
    investment.full_clean()
    investment.save()

    return investment


def investment_update(instance, **data) -> Investment:
    amount = instance.amount
    if data.get("is_submitted") is not None and instance.is_submitted == data.get("is_submitted"):
        raise ValidationError({"detail": _("Məlumatları doğru daxil edin")})
    if data.get("amount") is not None and instance.is_submitted is False:
        amount = data.get("amount")
        if amount <= 0:
            raise ValidationError({"detail": _("Məbləğ 0-dan böyük olmalıdır!")})

        if amount + instance.entrepreneur.amount_collected > instance.entrepreneur.total_investment:
            raise ValidationError({"detail": _("Məbləğ sifarişin yekun toplanmış məbləğindən çox ola bilməz")})

        profit = float(amount) * float(instance.entrepreneur.profit_ratio) / 100
        final_profit = float(amount) + float(profit)
        data['profit'] = profit
        data['final_profit'] = final_profit

        notification_create(user=instance.investor.user,
                            message=f"{instance.entrepreneur.project_name} sifarişinə etdiyiniz investisiyada dəyişiklik edildi, zəhmət olmasa profilinizə nəzər yetirin")

    if data.get("is_submitted") is not None and instance.is_submitted is False and data.get("is_submitted") is True:
        user_balance = user_balance_list().filter(user=instance.investor.user).last()
        company_balance = company_balance_list().last()
        if instance.is_from_debt_fund == False and data.get('is_from_debt_fund') == True:
            if data.get('amount_from_debt_fund') is not None:
                amount_from_debt = data.get('amount_from_debt_fund')
            else:
                amount_from_debt = instance.amount_from_debt_fund

            if float(amount_from_debt) > float(amount):
                raise ValidationError({"detail": _("Borc fondundan qarşılanacaq məbləğ yekun məbləğdən çox ola bilməz")})

            if float(amount_from_debt) > (float(company_balance.debt_fund) + float(company_balance.charity_fund)):
                raise ValidationError({"detail": "Fondda yetəri qədər məbləğ yoxdur"})
            else:
                if float(amount_from_debt) > float(company_balance.debt_fund):
                    deducated_amount = float(amount_from_debt) - float(company_balance.debt_fund)
                    company_balance.debt_fund = 0
                    company_balance.charity_fund = float(company_balance.charity_fund) - float(deducated_amount)
                    company_balance.save()
                else:
                    company_balance.debt_fund = float(company_balance.debt_fund) - float(amount_from_debt)
                    company_balance.save()

            if float(amount_from_debt) < float(amount):
                amount = float(amount) - float(amount_from_debt)
                if float(amount) == float(user_balance.balance):
                    instance.amount_must_send = 0
                    instance.amount_deducated_from_balance = float(amount)
                    instance.save()
                    user_balance.balance = float(user_balance.balance) - float(amount)
                    user_balance.save()
                elif float(amount) > float(user_balance.balance):
                    instance.amount_must_send = float(amount) - float(user_balance.balance)
                    instance.amount_deducated_from_balance = float(user_balance.balance)
                    instance.save()
                    user_balance.balance = 0
                    user_balance.save()
                elif float(amount) < float(user_balance.balance):
                    instance.amount_must_send = 0
                    instance.amount_deducated_from_balance = float(amount)
                    instance.save()
                    user_balance.balance = float(user_balance.balance) - float(amount)
                    user_balance.save()
            else:
                instance.amount_must_send = 0
                instance.amount_deducated_from_balance = 0
                instance.save()
        elif instance.is_from_debt_fund == True:
            if data.get('amount_from_debt_fund') is not None:
                if data.get('is_from_debt_fund') == False:
                    amount_from_debt = 0
                    instance.amount_from_debt_fund = 0
                    instance.save()
                    data['amount_from_debt_fund'] = 0
                amount_from_debt = data.get('amount_from_debt_fund')
            else:
                amount_from_debt = instance.amount_from_debt_fund


            if float(amount_from_debt) > float(amount):
                raise ValidationError({"detail": _("Borc fondundan qarşılanacaq məbləğ yekun məbləğdən çox ola bilməz")})

            if float(amount_from_debt) > (float(company_balance.debt_fund) + float(company_balance.charity_fund)):
                raise ValidationError({"detail": "Fondda yetəri qədər məbləğ yoxdur"})
            else:
                if float(amount_from_debt) > float(company_balance.debt_fund):
                    deducated_amount = float(amount_from_debt) - float(company_balance.debt_fund)
                    company_balance.debt_fund = 0
                    company_balance.charity_fund = float(company_balance.charity_fund) - float(deducated_amount)
                    company_balance.save()
                else:
                    company_balance.debt_fund = float(company_balance.debt_fund) - float(amount_from_debt)
                    company_balance.save()

            if float(amount_from_debt) < float(amount):
                amount = float(amount) - float(amount_from_debt)
                if float(amount) == float(user_balance.balance):
                    instance.amount_must_send = 0
                    instance.amount_deducated_from_balance = float(amount)
                    instance.save()
                    user_balance.balance = float(user_balance.balance) - float(amount)
                    user_balance.save()
                elif float(amount) > float(user_balance.balance):
                    instance.amount_must_send = float(amount) - float(user_balance.balance)
                    instance.amount_deducated_from_balance = float(user_balance.balance)
                    instance.save()
                    user_balance.balance = 0
                    user_balance.save()
                elif float(amount) < float(user_balance.balance):
                    instance.amount_must_send = 0
                    instance.amount_deducated_from_balance = float(amount)
                    instance.save()
                    user_balance.balance = float(user_balance.balance) - float(amount)
                    user_balance.save()
            else:
                instance.amount_must_send = 0
                instance.amount_deducated_from_balance = 0
                instance.save()
        else:
            if instance.is_from_debt_fund == False:
                if data.get('amount_from_debt_fund') is not None:
                    data['amount_from_debt_fund'] = 0
            if float(amount) == float(user_balance.balance):
                instance.amount_must_send = 0
                instance.amount_deducated_from_balance = float(amount)
                instance.save()
                user_balance.balance = float(user_balance.balance) - float(amount)
                user_balance.save()
            elif float(amount) > float(user_balance.balance):
                instance.amount_must_send = float(amount) - float(user_balance.balance)
                instance.amount_deducated_from_balance = float(user_balance.balance)
                instance.save()
                user_balance.balance = 0
                user_balance.save()
            elif float(amount) < float(user_balance.balance):
                instance.amount_must_send = 0
                instance.amount_deducated_from_balance = float(amount)
                instance.save()
                user_balance.balance = float(user_balance.balance) - float(amount)
                user_balance.save()

        instance.entrepreneur.amount_collected = float(instance.entrepreneur.amount_collected) + float(amount)
        instance.entrepreneur.save()
        notification_create(user=instance.investor.user, message=f"{instance.entrepreneur.project_name} sifarişinə etdiyiniz investisiya təsdiq edildi")

    if data.get("is_submitted") is not None and instance.is_submitted is True and data.get("is_submitted") is False:
        instance.entrepreneur.amount_collected = instance.entrepreneur.amount_collected - instance.amount
        instance.entrepreneur.save()
        user_balance = user_balance_list().filter(user=instance.investor.user).last()
        company_balance = company_balance_list().last()
        user_balance.balance = float(user_balance.balance) + float(instance.amount_deducated_from_balance)
        user_balance.save()
        if instance.is_from_debt_fund == True:
            amount_from_debt = instance.amount_from_debt_fund
            company_balance.debt_fund = float(company_balance.debt_fund) + float(amount_from_debt)
            company_balance.save()

        instance.amount_must_send = 0
        instance.amount_deducated_from_balance = 0
        instance.save()
        data['amount'] = instance.amount

        notification_create(user=instance.investor.user,
                            message=f"{instance.entrepreneur.project_name} sifarişinə etdiyiniz investisiyanın təsqilənməsi admin tərəfindən geri çəkildi")

    investment = investment_list().filter(pk=instance.pk).update(**data)

    return investment


def investment_delete(instance):
    if instance.is_submitted == True:
        if instance.is_from_debt_fund == True:
            company_balance = company_balance_list().last()
            amount_from_debt = instance.amount_from_debt_fund
            company_balance.debt_fund = float(company_balance.debt_fund) + float(amount_from_debt)
            company_balance.save()

        instance.entrepreneur.amount_collected = instance.entrepreneur.amount_collected - instance.amount
        instance.entrepreneur.save()
        user_balance = user_balance_list().filter(user=instance.investor.user).last()
        user_balance.balance = float(user_balance.balance) + float(instance.amount_deducated_from_balance)
        user_balance.save()

        instance.amount_must_send = 0
        instance.amount_deducated_from_balance = 0
        instance.save()

        notification_create(user=instance.investor.user,
                            message=f"{instance.entrepreneur.project_name} sifarişinə etdiyiniz investisiyanın təsqilənməsi admin tərəfindən geri çəkildi")

    instance.delete()


def investment_report_create(
        *, request_user,
        investor,
        investment,
        amount_want_to_send_to_cart: float = 0,
        amount_want_to_keep_in_the_balance: float = 0,
        amount_want_to_send_to_charity_fund: float = 0,
        amount_want_to_send_to_debt_fund: float = 0,
        note: str = None
) -> InvestmentReport:
    company_balance = company_balance_list().last()
    if (request_user.is_superuser is False and request_user.is_staff is False) and request_user != investor.user:
        raise ValidationError({'detail': _('Başqa investorun investisiya hesabatını edə bilməzsiniz')})

    if investment.is_from_debt_fund == True:
        company_balance.debt_fund = float(company_balance.debt_fund) + float(investment.amount_from_debt_fund)
        company_balance.save()
        amount_want_to_send_to_debt_fund = 0
        # amount_want_to_send_to_charity_fund = 0
        investment.final_profit = float(investment.final_profit) - float(investment.amount_from_debt_fund)

    total_amount = float(amount_want_to_send_to_cart) + float(amount_want_to_keep_in_the_balance) + float(amount_want_to_send_to_charity_fund) + float(
        amount_want_to_send_to_debt_fund)

    total_amount = float("{:.2f}".format(total_amount))
    final_profit = float("{:.2f}".format(investment.final_profit))

    if (
            amount_want_to_send_to_cart == 0 and amount_want_to_keep_in_the_balance == 0 and amount_want_to_send_to_charity_fund == 0 and amount_want_to_send_to_debt_fund == 0) and (
            float(total_amount) != float(final_profit)):
        logger.error('Bütün məbləğlər 0 daxil edilib')
        raise ValidationError({'detail': _('Məbləğləri doğru daxil edin')})

    if float(total_amount) != float(final_profit):
        logger.error('Yazılan məbləğlər ümumi gəlirə bərabər deyil')
        raise ValidationError({'detail': _('Məbləğləri doğru daxil edin')})

    investment_report_is_exists = investment_report_list().filter(investor=investor, investment=investment)

    if investment_report_is_exists.exists():
        investment_report = investment_report_is_exists.last()
        company_balance = company_balance_list().last()

        if investment_report.is_amount_sended_to_investor == True:
            raise ValidationError({'detail': _('Hesabat təsdiqləndiyi üçün dəyişiklik edə bilməzsiniz!')})

        # if investment.is_from_debt_fund == False:
        company_balance.debt_fund = float(company_balance.debt_fund) - float(investment_report.amount_want_to_send_to_debt_fund)
        company_balance.charity_fund = float(company_balance.charity_fund) - float(investment_report.amount_want_to_send_to_charity_fund)
        company_balance.save()

        user_balance = user_balance_list().filter(user=investment_report.investor.user).last()
        user_balance.balance = float(user_balance.balance) - float(investment_report.amount_want_to_keep_in_the_balance)
        user_balance.money_in_debt_fund = float(user_balance.money_in_debt_fund) - float(investment_report.amount_want_to_send_to_debt_fund)
        user_balance.save()

        investment_report.investor = investor
        investment_report.investment = investment
        investment_report.amount_want_to_send_to_cart = amount_want_to_send_to_cart
        investment_report.amount_want_to_keep_in_the_balance = amount_want_to_keep_in_the_balance
        investment_report.amount_want_to_send_to_charity_fund = amount_want_to_send_to_charity_fund
        investment_report.amount_want_to_send_to_debt_fund = amount_want_to_send_to_debt_fund
        investment_report.note = note
        investment_report.save()

        company_balance.debt_fund = float(company_balance.debt_fund) + float(amount_want_to_send_to_debt_fund)
        company_balance.charity_fund = float(company_balance.charity_fund) + float(amount_want_to_send_to_charity_fund)
        company_balance.save()

        user_balance.balance = float(user_balance.balance) + float(amount_want_to_keep_in_the_balance)
        user_balance.money_in_debt_fund = float(user_balance.money_in_debt_fund) + float(amount_want_to_send_to_debt_fund)
        user_balance.save()

    else:
        investment_report = InvestmentReport.objects.create(
            investor=investor, investment=investment, amount_want_to_send_to_cart=amount_want_to_send_to_cart,
            amount_want_to_keep_in_the_balance=amount_want_to_keep_in_the_balance, amount_want_to_send_to_charity_fund=amount_want_to_send_to_charity_fund,
            amount_want_to_send_to_debt_fund=amount_want_to_send_to_debt_fund, note=note
        )

        company_balance = company_balance_list().last()
        company_balance.debt_fund = float(company_balance.debt_fund) + float(amount_want_to_send_to_debt_fund)
        company_balance.charity_fund = float(company_balance.charity_fund) + float(amount_want_to_send_to_charity_fund)
        company_balance.save()

        user_balance = user_balance_list().filter(user=investment_report.investor.user).last()
        user_balance.balance = float(user_balance.balance) + float(amount_want_to_keep_in_the_balance)
        user_balance.money_in_debt_fund = float(user_balance.money_in_debt_fund) + float(amount_want_to_send_to_debt_fund)
        user_balance.save()

    return investment_report


def investment_report_update(instance, **data) -> InvestmentReport:
    investment_report = investment_report_list().filter(pk=instance.pk).update(**data)
    return investment_report
