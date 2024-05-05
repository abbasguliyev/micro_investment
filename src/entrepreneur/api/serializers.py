from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers
from entrepreneur.models import Entrepreneur, EntrepreneurImages
from entrepreneur.api.selectors import entrepreneur_list
from account.api.selectors import user_balance_list
from account.models import Investor
from investment.api.selectors import investment_report_list


class EntrepreneurCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = [
            'project_name', 'start_date', 'end_date', 'description',
            'count', 'purchase_price', 'sale_price', 'platform_cost_percentage',
            'investor_share_percentage', 'entrepreneur_share_percentage', 'debt_to_the_fund_percentage',
            'charity_to_the_fund_percentage'
        ]

        extra_kwargs = {
            'project_name': {'required': True},
            'start_date': {'required': True},
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
            'project_name', 'start_date', 'end_date', 'description',
            'count', 'purchase_price', 'sale_price', 'total_investment',
            'gross_income', 'platform_cost_percentage', 'platform_cost', 'final_profit',
            'investor_share_percentage', 'investor_share', 'entrepreneur_share_percentage', 'entrepreneur_share',
            'debt_to_the_fund_percentage', 'debt_to_the_fund',
            'charity_to_the_fund_percentage', 'charity_to_the_fund', 'profit_ratio',
            'is_active', 'finished_date', 'amount_collected', 'is_finished'
        ]
        extra_kwargs = {
            'project_name': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'count': {'required': False},
            'purchase_price': {'required': False},
            'sale_price': {'required': False},
            'gross_income': {'required': False},
            'platform_cost_percentage': {'required': False},
            'platform_cost': {'required': False},
            'final_profit': {'required': False},
            'investor_share_percentage': {'required': False},
            'investor_share': {'required': False},
            'entrepreneur_share_percentage': {'required': False},
            'entrepreneur_share': {'required': False},
            'debt_to_the_fund_percentage': {'required': False},
            'debt_to_the_fund': {'required': False},
            'charity_to_the_fund_percentage': {'required': False},
            'charity_to_the_fund': {'required': False},
            'profit_ratio': {'required': False},
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

    class InlineEntrepreneurOwnerSerializer(serializers.ModelSerializer):
        class EntrepreneurInlineUserOutSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ['id', 'first_name', 'last_name', 'email']

        user = EntrepreneurInlineUserOutSerializer(read_only=True)

        class Meta:
            model = Investor
            fields = [
                'id', 'user'
            ]

    owner = InlineEntrepreneurOwnerSerializer()
    images = EntrepreneurNestedImagesSerializer(many=True)

    total_charity_money = serializers.SerializerMethodField('get_total_charity_money')

    def get_total_charity_money(self, instance):
        investment_reports = investment_report_list().filter(investment__entrepreneur=instance)
        if len(investment_reports) > 0:
            total_charity_money = investment_reports.aggregate(total_charity_money=Sum('amount_want_to_send_to_charity_fund'))
            return total_charity_money.get('total_charity_money')
        else:
            return 0

    class Meta:
        model = Entrepreneur
        fields = [
            'id', 'owner', 'project_name', 'start_date', 'end_date', 'finished_date', 'description',
            'is_active', 'count', 'purchase_price', 'sale_price', 'total_investment', 'gross_income',
            'platform_cost_percentage',
            'platform_cost', 'final_profit', 'investor_share_percentage', 'investor_share',
            'entrepreneur_share_percentage', 'entrepreneur_share',
            'debt_to_the_fund_percentage', 'debt_to_the_fund', 'charity_to_the_fund_percentage', 'charity_to_the_fund',
            'profit_ratio', 'amount_collected', 'images', 'investments', 'is_finished', 'total_charity_money'
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
