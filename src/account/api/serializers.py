from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import Investor, Experience, Education, UserBalance, CompanyBalance
from account.api.selectors import user_list, user_balance_list


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }


class UserOutSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField('get_balance')

    def get_balance(self, instance):
        balance_list = user_balance_list().filter(user=instance).last()
        if balance_list is not None:
            return balance_list.balance
        else:
            return 0

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'balance']


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class InvestorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    references = serializers.CharField(required=False)

    class Meta:
        model = Investor
        fields = [
            'first_name', 'last_name', 'email', 'password', 'birthdate', 'address',
            'marital_status', 'employment_status', 'housing_status', 'phone_number',
            'credit_cart_number', 'debt_amount', 'monthly_income', 'references',
            'profile_picture', 'about', 'business_activities'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'birthdate': {'required': True},
            'address': {'required': True},
            'credit_cart_number': {'required': True},
            'references': {'required': False},
            'profile_picture': {'required': False},
            'about': {'required': False},
            'business_activities': {'required': False},
        }


class InvestorUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_active = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    email = serializers.CharField()

    class Meta:
        model = Investor
        fields = [
            'first_name', 'last_name', 'email', 'birthdate', 'address',
            'marital_status', 'employment_status', 'housing_status', 'phone_number',
            'credit_cart_number', 'debt_amount', 'monthly_income', 'references',
            'profile_picture', 'about', 'business_activities', 'is_active', 'is_superuser'
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'birthdate': {'required': False},
            'address': {'required': False},
            'credit_cart_number': {'required': False},
            'references': {'required': False},
            'profile_picture': {'required': False},
            'about': {'required': False},
            'business_activities': {'required': False},
            'is_active': {'required': False},
            'is_superuser': {'required': False}
        }


class InvestorOutSerializer(serializers.ModelSerializer):
    user = UserOutSerializer(read_only=True)
    references = UserOutSerializer(read_only=True, many=True)

    class Meta:
        model = Investor
        fields = [
            'id', 'user', 'birthdate', 'address', 'marital_status', 'employment_status',
            'housing_status', 'phone_number', 'credit_cart_number', 'debt_amount',
            'monthly_income', 'references', 'profile_picture', 'about',
            'business_activities'
        ]


class ExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'experience_place', 'position', 'description',
            'city', 'start_year', 'end_year', 'is_continue'
        ]

        extra_kwargs = {
            'experience_place': {'required': True},
            'position': {'required': True},
            'city': {'required': True},
            'start_year': {'required': True},
            'is_continue': {'required': True},
        }


class ExperienceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'experience_place', 'position', 'description',
            'city', 'start_year', 'end_year', 'is_continue'
        ]

        extra_kwargs = {
            'experience_place': {'required': False},
            'position': {'required': False},
            'city': {'required': False},
            'start_year': {'required': False},
            'is_continue': {'required': False},
        }


class ExperienceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id', 'user', 'experience_place', 'position', 'description',
            'city', 'start_year', 'end_year', 'is_continue'
        ]


class EducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'education_place', 'education_branch',
            'city', 'start_year', 'end_year', 'is_continue'
        ]

        extra_kwargs = {
            'education_place': {'required': True},
            'education_branch': {'required': True},
            'city': {'required': True},
            'start_year': {'required': True},
            'is_continue': {'required': True},
        }


class EducationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'education_place', 'education_branch',
            'city', 'start_year', 'end_year', 'is_continue'
        ]

        extra_kwargs = {
            'education_place': {'required': False},
            'education_branch': {'required': False},
            'city': {'required': False},
            'start_year': {'required': False},
            'is_continue': {'required': False},
        }


class EducationOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'user', 'education_place', 'education_branch',
            'city', 'start_year', 'end_year', 'is_continue'
        ]


class UserBalanceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ['id', 'user', 'balance']

class CompanyBalanceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBalance
        fields = ['id', 'debt_fund', 'charity_fund']
