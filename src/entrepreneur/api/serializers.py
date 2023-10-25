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
    entrepreneur_form = serializers.PrimaryKeyRelatedField(
        queryset = entrepreneur_form_list(), write_only=True
    )
    class Meta:
        model = Entrepreneur
        fields = ['project_name', 'target_amount', 'end_date', 'description', 'entrepreneur_form', 'income']

class EntrepreneurUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = ['project_name', 'target_amount', 'end_date', 'description', 'is_active', 'income']
        extra_kwargs = {
            'project_name': {'required': False},
            'target_amount': {'required': False},
            'end_date': {'required': False},
            'description': {'required': False},
            'is_active': {'required': False},
            'income': {'required': False},
        }

class EntrepreneurOutSerializer(serializers.ModelSerializer):
    class EntrepreneurNestedImagesSerializer(serializers.ModelSerializer):
        class Meta:
            model = EntrepreneurImages
            fields = ['id', 'image']

    owner = InvestorOutSerializer()
    entrepreneur_form = EntrepreneurFormOutSerializer()
    images = EntrepreneurNestedImagesSerializer(many=True)

    class Meta:
        model = Entrepreneur
        fields = ['id', 'images', 'owner', 'project_name', 'target_amount', 'amount_collected', 'start_date', 'end_date', 'description', 'entrepreneur_form', 'is_active', 'income']

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
    entrepreneur = EntrepreneurOutSerializer()

    class Meta:
        model = EntrepreneurImages
        fields = ['id', 'entrepreneur', 'image']
