from rest_framework import serializers
from django.db.models import Sum, Q
from django.contrib.auth import get_user_model
from account.models import Investor, Experience, Education, UserBalance, CompanyBalance
from account.api.selectors import user_list, user_balance_list, investor_list
from investment.api.selectors import investment_list, investment_report_list


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
    money_in_debt_fund = serializers.SerializerMethodField('get_money_in_debt_fund')

    def get_balance(self, instance):
        balance_list = user_balance_list().filter(user=instance).last()
        if balance_list is not None:
            return balance_list.balance
        else:
            return 0

    def get_money_in_debt_fund(self, instance):
        balance_list = user_balance_list().filter(user=instance).last()
        if balance_list is not None:
            return balance_list.money_in_debt_fund
        else:
            return 0

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'balance', 'money_in_debt_fund']


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    investor = serializers.PrimaryKeyRelatedField(
        queryset=investor_list(), write_only=True, allow_null=True, allow_empty=True
    )
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

    own_investment = serializers.SerializerMethodField()
    investment_count = serializers.SerializerMethodField()
    profit_earned = serializers.SerializerMethodField()
    money_given_to_a_debt_fund_count = serializers.SerializerMethodField()
    money_given_to_a_charity_fund_count = serializers.SerializerMethodField()

    def get_investment_count(self, instance):
        result = investment_list().filter(investor=instance.id).aggregate(
            total_amount=Sum('amount', filter=Q(investor=instance))
        )
        total_amount = result.get('total_amount')
        if total_amount is None:
            total_amount = 0

        total_amount = "%.2f" % total_amount
        return total_amount

    def get_profit_earned(self, instance):
        result = investment_list().filter(investor=instance.id).aggregate(
            total_profit=Sum('profit', filter=Q(investor=instance))
        )
        total_profit = result.get('total_profit')
        if total_profit is None:
            total_profit = 0

        total_profit = "%.2f" % total_profit
        return total_profit

    def get_own_investment(self, instance):
        result = investment_list().filter(investor=instance.id, is_amount_sended=True).aggregate(
            total_own_investment=Sum('amount_must_send', filter=Q(investor=instance.id, is_amount_sended=True))
        )
        total_own_investment = result.get('total_own_investment')
        if total_own_investment is None:
            total_own_investment = 0

        total_own_investment = "%.2f" % total_own_investment
        return total_own_investment

    def get_money_given_to_a_debt_fund_count(self, instance):
        result = investment_report_list().filter(investor=instance.id).aggregate(
            total_amount_want_to_send_to_debt_fund=Sum('amount_want_to_send_to_debt_fund', filter=Q(investor=instance.id))
        )
        total_amount_want_to_send_to_debt_fund = result.get('total_amount_want_to_send_to_debt_fund')
        if total_amount_want_to_send_to_debt_fund is None:
            total_amount_want_to_send_to_debt_fund = 0

        total_amount_want_to_send_to_debt_fund = "%.2f" % total_amount_want_to_send_to_debt_fund
        return total_amount_want_to_send_to_debt_fund

    def get_money_given_to_a_charity_fund_count(self, instance):
        result = investment_report_list().filter(investor=instance.id).aggregate(
            total_amount_want_to_send_to_charity_fund=Sum('amount_want_to_send_to_charity_fund', filter=Q(investor=instance.id))
        )
        total_amount_want_to_send_to_charity_fund = result.get('total_amount_want_to_send_to_charity_fund')
        if total_amount_want_to_send_to_charity_fund is None:
            total_amount_want_to_send_to_charity_fund = 0

        total_amount_want_to_send_to_charity_fund = "%.2f" % total_amount_want_to_send_to_charity_fund
        return total_amount_want_to_send_to_charity_fund

    class Meta:
        model = Investor
        fields = [
            'id', 'user', 'birthdate', 'address', 'marital_status', 'employment_status',
            'housing_status', 'phone_number', 'credit_cart_number', 'debt_amount',
            'monthly_income', 'references', 'profile_picture', 'about',
            'business_activities', 'investment_count', 'own_investment', 'money_given_to_a_debt_fund_count',
            'money_given_to_a_charity_fund_count', 'profit_earned'
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
        fields = ['id', 'user', 'balance', 'money_in_debt_fund']


class CompanyBalanceOutSerializer(serializers.ModelSerializer):
    total_fund_money = serializers.SerializerMethodField('get_total_fund_money')

    def get_total_fund_money(self, instance):
        investments = investment_list().filter(is_from_debt_fund=True, entrepreneur__is_finished=False)
        if len(investments) > 0:
            total_fund_money = investments.aggregate(total_fund_money=Sum('amount_from_debt_fund'))
            return total_fund_money.get('total_fund_money')
        else:
            return 0

    class Meta:
        model = CompanyBalance
        fields = ['id', 'debt_fund', 'charity_fund', 'total_fund_money']


class DebtFundExpenseSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), write_only=True
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
