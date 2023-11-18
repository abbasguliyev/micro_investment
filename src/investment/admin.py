from django.contrib import admin
from investment.models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'entrepreneur', 'amount', 'profit', 'final_profit', 'investment_date', 'is_submitted')
