from django.contrib.auth import get_user_model
from django.db.models import Sum
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
        fields = ['investor', 'entrepreneur', 'amount', 'is_submitted', 'is_from_debt_fund', 'amount_from_debt_fund']


class InvestmentUpdateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True, allow_null=True, allow_empty=True
    )
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset=entrepreneur_list(), write_only=True
    )

    class Meta:
        model = Investment
        fields = ['investor', 'entrepreneur', 'amount', 'is_submitted', 'is_amount_sended', 'is_amount_sended_submitted', 'is_from_debt_fund', 'amount_from_debt_fund']
        extra_kwargs = {
            'investor': {'required': False},
            'entrepreneur': {'required': False},
            'amount': {'required': False},
            'is_submitted': {'required': False},
            'is_amount_sended': {'required': False},
            'is_from_debt_fund': {'required': False},
            'amount_from_debt_fund': {'required': False},
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
                  'is_submitted', 'investment_report', 'is_amount_sended', 'is_amount_sended_submitted', 'is_from_debt_fund', 'amount_from_debt_fund']


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
    class Meta:
        model = InvestmentReport
        fields = ['is_amount_sended_to_investor']
        extra_kwargs = {
            'is_amount_sended_to_investor': {'required': False}
        }


class InvestmentReportOutSerializer(serializers.ModelSerializer):
    class InvestmentReportInvestorInlineSerializer(serializers.ModelSerializer):
        class InvestmentReportInvestorUserInlineSerializer(serializers.ModelSerializer):
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

        user = InvestmentReportInvestorUserInlineSerializer()

        class Meta:
            model = Investor
            fields = ['id', 'user', 'credit_cart_number']

    investor = InvestmentReportInvestorInlineSerializer()

    class Meta:
        model = InvestmentReport
        fields = ['id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                  'amount_want_to_send_to_debt_fund', 'note', 'is_amount_sended_to_investor']
