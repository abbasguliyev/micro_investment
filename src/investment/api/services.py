from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from investment.models import Investment, InvestmentReport
from investment.api.selectors import investment_list, investment_report_list
from account.api.selectors import company_balance_list, user_balance_list
from account.api.services import company_balance_create

def investment_create(
        *, request_user, investor,
        entrepreneur,
        amount: float,
        is_submitted: bool = False
) -> Investment:
    if amount <= 0:
        raise ValidationError({"detail": _("Məbləğ 0-dan böyük olmalıdır!")})

    if amount + entrepreneur.amount_collected > entrepreneur.total_investment:
        raise ValidationError({"detail": _("Məbləğ sifarişin yekun toplanmış məbləğindən çox ola bilməz")})

    has_investment = investment_list().filter(investor=investor, entrepreneur=entrepreneur).exists()
    if has_investment:
        raise ValidationError({"detail": _("Eyni sifarişə yalnız 1 dəfə yatırım edə bilərsiniz")})

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
        is_submitted=is_submitted
    )
    investment.full_clean()
    investment.save()

    return investment


def investment_update(instance, **data) -> Investment:
    investment = investment_list().filter(pk=instance.pk).update(**data)
    amount = instance.amount
    print(f"{amount=}")
    print(f"{instance.amount=}")
    if data.get("is_submitted") is not None and instance.is_submitted == data.get("is_submitted"):
        raise ValidationError({"detail": _("Məlumatları doğru daxil edin")})
    if data.get("amount") is not None and data.get("is_submitted") is True:
        amount = data.get("amount")
        if amount <= 0:
            raise ValidationError({"detail": _("Məbləğ 0-dan böyük olmalıdır!")})

        if amount + instance.entrepreneur.amount_collected > instance.entrepreneur.total_investment:
            raise ValidationError({"detail": _("Məbləğ sifarişin yekun toplanmış məbləğindən çox ola bilməz")})

        profit = float(amount) * float(instance.entrepreneur.profit_ratio) / 100
        final_profit = float(amount) + float(profit)
        data['profit'] = profit
        data['final_profit'] = profit
    if data.get("is_submitted") is not None and instance.is_submitted is False and data.get("is_submitted") is True:
        instance.entrepreneur.amount_collected = instance.entrepreneur.amount_collected + amount
        instance.entrepreneur.save()
    if data.get("is_submitted") is not None and instance.is_submitted is True and data.get("is_submitted") is False:
        instance.entrepreneur.amount_collected = instance.entrepreneur.amount_collected - instance.amount
        instance.entrepreneur.save()
    return investment


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
    if (request_user.is_superuser is False and request_user.is_staff is False) and request_user != investor.user:
        raise ValidationError({'detail': _('Başqa investorun investisiya hesabatını edə bilməzsiniz')})

    total_amount = float(amount_want_to_send_to_cart) + float(amount_want_to_keep_in_the_balance) + float(amount_want_to_send_to_charity_fund) + float(
        amount_want_to_send_to_debt_fund)

    if (amount_want_to_send_to_cart == 0 and amount_want_to_keep_in_the_balance == 0 and amount_want_to_send_to_charity_fund == 0 and amount_want_to_send_to_debt_fund
        == 0) and (float(total_amount) != float(investment.final_profit)):
        raise ValidationError({'detail': _('Məbləğləri doğru daxil edin')})

    if float(total_amount) != float(investment.final_profit):
        print(f"{total_amount=}")
        print(f"{investment.final_profit=}")
        raise ValidationError({'detail': _('Məbləğləri doğru daxil edin')})

    investment_report_is_exists = investment_report_list().filter(investor=investor, investment=investment)

    if investment_report_is_exists.exists():
        investment_report = investment_report_is_exists.last()
        investment_report.investor = investor
        investment_report.investment = investment
        investment_report.amount_want_to_send_to_cart = amount_want_to_send_to_cart
        investment_report.amount_want_to_keep_in_the_balance = amount_want_to_keep_in_the_balance
        investment_report.amount_want_to_send_to_charity_fund = amount_want_to_send_to_charity_fund
        investment_report.amount_want_to_send_to_debt_fund = amount_want_to_send_to_debt_fund
        investment_report.note = note
        investment_report.save()
        
        company_balance = company_balance_list().last()

        company_balance.debt_fund = float(company_balance.debt_fund) - float(investment_report.amount_want_to_send_to_debt_fund)
        company_balance.charity_fund = float(company_balance.charity_fund) - float(investment_report.amount_want_to_send_to_charity_fund)
        company_balance.save()

        company_balance.debt_fund = float(company_balance.debt_fund) + float(amount_want_to_send_to_debt_fund)
        company_balance.charity_fund = float(company_balance.charity_fund) + float(amount_want_to_send_to_charity_fund)
        company_balance.save()

        user_balance = user_balance_list().filter(user=investment_report.investor).last()

        user_balance.balance = float(user_balance.balance) - float(investment_report.amount_want_to_keep_in_the_balance)
        user_balance.save()

        user_balance.balance = float(user_balance.balance) + float(amount_want_to_keep_in_the_balance)
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

        user_balance = user_balance_list().filter(user=investment_report.investor).last()
        user_balance.balance = float(user_balance.balance) + float(amount_want_to_keep_in_the_balance)
        user_balance.save()
    
    return investment_report


def investment_report_update(instance, **data) -> InvestmentReport:
    investment_report = investment_report_list().filter(pk=instance.pk).update(**data)
    return investment_report
