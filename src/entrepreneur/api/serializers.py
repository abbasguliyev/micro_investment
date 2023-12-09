from django.contrib.auth import get_user_model
from rest_framework import serializers
from entrepreneur.models import Entrepreneur, EntrepreneurImages
from entrepreneur.api.selectors import entrepreneur_list
from account.api.serializers import InvestorOutSerializer
from account.models import Investor
from investment.models import Investment, InvestmentReport


class EntrepreneurCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = [
            'project_name', 'end_date', 'description',
            'count', 'purchase_price', 'sale_price', 'platform_cost_percentage',
            'investor_share_percentage', 'entrepreneur_share_percentage', 'debt_to_the_fund_percentage',
            'charity_to_the_fund_percentage'
        ]

        extra_kwargs = {
            'project_name': {'required': True},
            'end_date': {'required': True},
            'count': {'required': True},
            'purchase_price': {'required': True},
            'sale_price': {'required': True},
            'platform_cost_percentage': {'required': True},
            'investor_share_percentage': {'required': True},
            'entrepreneur_share_percentage': {'required': True}
        }


class EntrepreneurUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = [
            'is_active', 'finished_date', 'amount_collected', 'is_finished'
        ]
        extra_kwargs = {
            'is_active': {'required': False},
            'finished_date': {'required': False},
            'amount_collected': {'required': False},
            'is_finished': {'required': False}
        }


class EntrepreneurOutSerializer(serializers.ModelSerializer):
    class EntrepreneurNestedImagesSerializer(serializers.ModelSerializer):
        class Meta:
            model = EntrepreneurImages
            fields = ['id', 'image']

    class InvestmentNestedSerializer(serializers.ModelSerializer):
        class InvestmentInvestorInlineSerializer(serializers.ModelSerializer):
            class InvestmentInvestorUserInlineSerializer(serializers.ModelSerializer):
                class Meta:
                    model = get_user_model()
                    fields = ['id', 'first_name', 'last_name']

            user = InvestmentInvestorUserInlineSerializer()

            class Meta:
                model = Investor
                fields = ['id', 'user']

        class InvestmentReportInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = InvestmentReport
                fields = ['id', 'investor', 'investment', 'amount_want_to_send_to_cart', 'amount_want_to_keep_in_the_balance', 'amount_want_to_send_to_charity_fund',
                          'amount_want_to_send_to_debt_fund', 'note']

        investor = InvestmentInvestorInlineSerializer()
        investment_report = InvestmentReportInlineSerializer(many=True)

        class Meta:
            model = Investment
            fields = ['id', 'investor', 'entrepreneur', 'amount', 'profit', 'final_profit', 'investment_date',
                      'is_submitted', 'investment_report']

    owner = InvestorOutSerializer()
    images = EntrepreneurNestedImagesSerializer(many=True)
    investments = InvestmentNestedSerializer(many=True)

    class Meta:
        model = Entrepreneur
        fields = [
            'id', 'owner', 'project_name', 'start_date', 'end_date', 'finished_date', 'description',
            'is_active', 'count', 'purchase_price', 'sale_price', 'total_investment', 'gross_income',
            'platform_cost_percentage',
            'platform_cost', 'final_profit', 'investor_share_percentage', 'investor_share',
            'entrepreneur_share_percentage', 'entrepreneur_share',
            'debt_to_the_fund_percentage', 'debt_to_the_fund', 'charity_to_the_fund_percentage', 'charity_to_the_fund',
            'profit_ratio', 'amount_collected', 'images', 'investments', 'is_finished'
        ]


class EntrepreneurImagesCreateSerializer(serializers.ModelSerializer):
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset=entrepreneur_list(), write_only=True
    )

    class Meta:
        model = EntrepreneurImages
        fields = ['entrepreneur', 'image']


class EntrepreneurImagesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurImages
        fields = ['image']


class EntrepreneurImagesOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurImages
        fields = ['id', 'entrepreneur', 'image']
