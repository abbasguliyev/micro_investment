from django.contrib.auth import get_user_model
from rest_framework import serializers
from investment.models import Investment
from account.models import Investor
from entrepreneur.models import Entrepreneur
from investment.api.selectors import investment_list
from account.api.serializers import InvestorOutSerializer
from account.api.selectors import investor_list
from entrepreneur.api.selectors import entrepreneur_list
from entrepreneur.api.serializers import EntrepreneurOutSerializer

class InvestmentCreateSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset = investor_list(), write_only=True, allow_null=True, allow_empty=True
    )
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset = entrepreneur_list(), write_only=True
    )
    class Meta:
        model = Investment
        fields = ['investor', 'entrepreneur', 'amount', 'is_submitted']

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
            fields = ['id', 'project_name', 'profit_ratio', 'start_date', 'end_date',]
    

    investor = InvestorInlineSerializer()
    entrepreneur = EntrepreneurInlineOutSerializer()
    class Meta:
        model = Investment
        fields = ['id', 'investor', 'entrepreneur', 'amount', 'profit', 'final_profit', 'investment_date', 'is_submitted']