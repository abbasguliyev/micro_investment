from rest_framework import serializers
from investment.models import Investment
from investment.api.selectors import investment_list
from account.api.serializers import InvestorOutSerializer
from entrepreneur.api.selectors import entrepreneur_list
from entrepreneur.api.serializers import EntrepreneurOutSerializer

class InvestmentCreateSerializer(serializers.ModelSerializer):
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset = entrepreneur_list(), write_only=True
    )
    class Meta:
        model = Investment
        fields = ['entrepreneur', 'amount']

class InvestmentOutSerializer(serializers.ModelSerializer):
    investor = InvestorOutSerializer()
    entrepreneur = EntrepreneurOutSerializer()
    class Meta:
        model = Investment
        fields = ['id', 'investor', 'entrepreneur', 'amount', 'income']