from rest_framework import serializers
from entrepreneur.models import EntrepreneurForm, Entrepreneur, EntrepreneurImages
from entrepreneur.api.selectors import entrepreneur_form_list, entrepreneur_list
from account.api.selectors import investor_list
from account.api.serializers import InvestorOutSerializer

class EntrepreneurFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurForm
        fields = ['title', 'is_active', 'questions']

class EntrepreneurFormUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurForm
        fields = ['title', 'is_active', 'questions']
        extra_kwargs = {
            'title': {'required': False},
            'is_active': {'required': False},
            'questions': {'required': False},
        }

class EntrepreneurFormOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurForm
        fields = ['id', 'title', 'is_active', 'questions']

class EntrepreneurCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = [
            'project_name', 'end_date', 'description', 'entrepreneur_form', 
            'count', 'purchase_price', 'sale_price', 'platform_cost_percentage',
            'investor_share_percentage', 'entrepreneur_share_percentage', 'debt_to_the_fund_percentage',
            'charity_to_the_fund_percentage'
        ]

        extra_kwargs = {
            'project_name': {'required': True},
            'end_date': {'required': True},
            'entrepreneur_form': {'required': True},
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
            'is_active', 'finished_date', 'amount_collected'
        ]
        extra_kwargs = {
            'is_active': {'required': False},
            'finished_date': {'required': False},
            'amount_collected': {'required': False}
        }

class EntrepreneurOutSerializer(serializers.ModelSerializer):
    class EntrepreneurNestedImagesSerializer(serializers.ModelSerializer):
        class Meta:
            model = EntrepreneurImages
            fields = ['id', 'image']

    owner = InvestorOutSerializer()
    images = EntrepreneurNestedImagesSerializer(many=True)

    class Meta:
        model = Entrepreneur
        fields = [
            'id', 'owner', 'project_name', 'start_date', 'end_date', 'finished_date', 'description', 'entrepreneur_form', 
            'is_active', 'count', 'purchase_price', 'sale_price', 'total_investment', 'gross_income', 'platform_cost_percentage',
            'platform_cost', 'final_profit', 'investor_share_percentage', 'investor_share', 'entrepreneur_share_percentage', 'entrepreneur_share',
            'debt_to_the_fund_percentage', 'debt_to_the_fund', 'charity_to_the_fund_percentage', 'charity_to_the_fund',
            'profit_ratio', 'amount_collected', 'images'
        ]

class EntrepreneurImagesCreateSerializer(serializers.ModelSerializer):
    entrepreneur = serializers.PrimaryKeyRelatedField(
        queryset = entrepreneur_list(), write_only=True
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
