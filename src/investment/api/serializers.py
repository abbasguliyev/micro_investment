from django.contrib.auth import get_user_model
from rest_framework import serializers
from investment.models import Investment, InvestmentReport
from account.models import Investor
from entrepreneur.models import Entrepreneur
from investment.api.selectors import investment_list
from account.api.serializers import InvestorOutSerializer
from account.api.selectors import investor_list
from entrepreneur.api.selectors import entrepreneur_list
from entrepreneur.api.serializers import EntrepreneurOutSerializer


class InvestmentCreateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True, allow_null=True, allow_empty=True
    )
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset=entrepreneur_list(), write_only=True
    )

    class Meta:
        model = Investment
        fields = ['investor', 'entrepreneur', 'amount', 'is_submitted']


class InvestmentUpdateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True, allow_null=True, allow_empty=True
    )
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset=entrepreneur_list(), write_only=True
    )

    class Meta:
        model = Investment
        fields = ['investor', 'entrepreneur', 'amount', 'is_submitted']
        extra_kwargs = {
            'investor': {'required': False},
            'entrepreneur': {'required': False},
            'amount': {'required': False},
            'is_submitted': {'required': False}
        }


class InvestmentOutSerializer(serializers.ModelSerializer):
    class InvestorInlineSerializer(serializers.ModelSerializer):
        class UserInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ['id', 'first_name', 'last_name']

        user = UserInlineSerializer()

        class Meta:
            model = Investor
            fields = ['id', 'user']

    class EntrepreneurInlineOutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Entrepreneur
            fields = ['id', 'project_name', 'profit_ratio', 'start_date', 'end_date', 'is_finished', 'is_active', 'finished_date']

    investor = InvestorInlineSerializer()
    entrepreneur = EntrepreneurInlineOutSerializer()

    class Meta:
        model = Investment
        fields = ['id', 'investor', 'entrepreneur', 'amount', 'profit', 'final_profit', 'investment_date',
                  'is_submitted']


class InvestmentReportCreateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True
    )
    investment = serializers.PrimaryKeyRelatedField(
        queryset=investment_list(), write_only=True
    )

    class Meta:
        model = InvestmentReport
        fields = ['investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                  'amount_want_to_send_to_debt_fund', 'note']


class InvestmentReportUpdateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True
    )
    investment = serializers.PrimaryKeyRelatedField(
        queryset=investment_list(), write_only=True
    )

    class Meta:
        model = InvestmentReport
        fields = ['investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                  'amount_want_to_send_to_debt_fund', 'note']
        extra_kwargs = {
            'investor': {'required': False},
            'investment': {'required': False},
            'amount_want_to_send_to_cart': {'required': False},
            'amount_want_to_keep_in_the_balance': {'required': False},
            'amount_want_to_send_to_charity_fund': {'required': False},
            'amount_want_to_send_to_debt_fund': {'required': False},
            'note': {'required': False}
        }


class InvestmentReportOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentReport
        fields = ['id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                  'amount_want_to_send_to_debt_fund', 'note']