from django.contrib import admin
from investment.models import Investment, InvestmentReport


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'entrepreneur', 'amount', 'amount_must_send', 'amount_deducated_from_balance', 'profit', 'final_profit', 'investment_date', 'is_submitted', 'is_amount_sended', 'is_amount_sended_submitted', 'is_from_debt_fund', 'amount_from_debt_fund')
    list_filter = ('investor', 'entrepreneur')

@admin.register(InvestmentReport)
class InvestmentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                    'amount_want_to_send_to_debt_fund', 'note', 'is_amount_sended_to_investor')
