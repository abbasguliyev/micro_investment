from django.contrib.auth import get_user_model
from rest_framework import serializers
from investment.models import Investment, InvestmentReport
from account.models import Investor
from entrepreneur.models import Entrepreneur
from investment.api.selectors import investment_list
from account.api.selectors import investor_list, user_balance_list
from entrepreneur.api.selectors import entrepreneur_list


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
            balance = serializers.SerializerMethodField('get_balance')

            def get_balance(self, instance):
                balance_list = user_balance_list().filter(user=instance).last()
                if balance_list is not None:
                    return balance_list.balance
                else:
                    return 0
                
            class Meta:
                model = get_user_model()
                fields = ['id', 'first_name', 'last_name', 'balance']

        user = UserInlineSerializer()

        class Meta:
            model = Investor
            fields = ['id', 'user']

    class EntrepreneurInlineOutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Entrepreneur
            fields = ['id', 'project_name', 'profit_ratio', 'start_date', 'end_date', 'is_finished', 'is_active', 'finished_date']

    class InvestmentReportInlineOutSerializer(serializers.ModelSerializer):
        class Meta:
            model = InvestmentReport
            fields = ['id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                      'amount_want_to_send_to_debt_fund', 'note']

    investor = InvestorInlineSerializer()
    entrepreneur = EntrepreneurInlineOutSerializer()
    investment_report = InvestmentReportInlineOutSerializer(many=True)

    class Meta:
        model = Investment
        fields = ['id', 'investor', 'entrepreneur', 'amount', 'amount_must_send', 'amount_deducated_from_balance', 'profit', 'final_profit', 'investment_date',
                  'is_submitted', 'investment_report']


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
