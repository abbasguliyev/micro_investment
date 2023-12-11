from django.contrib import admin
from investment.models import Investment, InvestmentReport


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'entrepreneur', 'amount', 'profit', 'final_profit', 'investment_date', 'is_submitted')


@admin.register(InvestmentReport)
class InvestmentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                    'amount_want_to_send_to_debt_fund', 'note')
