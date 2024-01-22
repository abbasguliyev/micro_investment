from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import Investor, Experience, Education, UserBalance, CompanyBalance


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'email')


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'money_in_debt_fund')
    list_display_links = ('id', 'user')


@admin.register(CompanyBalance)
class CompanyBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'debt_fund', 'charity_fund')
    list_display_links = ('id',)
