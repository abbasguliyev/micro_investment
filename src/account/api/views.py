from django.utils.translation import gettext_lazy as _
from django.contrib.auth import user_logged_in

from rest_framework.response import Response

from rest_framework.views import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django_filters.rest_framework import DjangoFilterBackend

from account.api import serializers, selectors, services, utils, filters


class LoginView(TokenObtainPairView):
    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        default_error_messages = {
            'no_active_account': _('Hesabı təsdiqlənmiş istifadəçi tapılmadı')
        }
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs) -> Response:
        data = super().post(request, *args, **kwargs)

        data = data.data
        access_token = utils.jwt_decode_handler(data.get('access'))

        if not selectors.user_list().filter(pk=access_token.get("user_id")).last():
            return Response({"error": True, "detail": _("İstifadəçi tapılmadı")}, status=status.HTTP_404_NOT_FOUND)

        user = selectors.user_list().filter(pk=access_token.get("user_id")).last()
        user_logged_in.send(sender=type(user), request=request, user=user)

        user_details = serializers.UserOutSerializer(user)
        data['user_details'] = user_details.data
        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = selectors.investor_list()
    serializer_class = serializers.InvestorOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.InvestorFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.InvestorCreateSerializer
        elif self.action == 'update':
            return serializers.InvestorUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.investor_create(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.investor_update(request_user=request.user, instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, serializer_class=serializers.InvestorOutSerializer, filterset_class=None, pagination_class=None)
    def me(self, request, *args, **kwargs):
        user = request.user
        investor = selectors.investor_list().filter(user=user).last()
        serializers = self.get_serializer(investor)
        return Response(serializers.data)
    
    @action(methods=["POST"], detail=False, serializer_class=serializers.ChangePasswordSerializer, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Yanlış şifrə."]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(data={'detail': _("Password updated successfully")}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        print(f"{user=}")
        self.perform_destroy(instance)
        selectors.user_list().filter(pk=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = selectors.experience_list()
    serializer_class = serializers.ExperienceOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ExperienceFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ExperienceCreateSerializer
        elif self.action == 'update':
            return serializers.ExperienceUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        investor = selectors.investor_list().filter(user=request.user).last()
        services.experience_create(user=investor, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.experience_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)


class EducationViewSet(viewsets.ModelViewSet):
    queryset = selectors.education_list()
    serializer_class = serializers.EducationOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.EducationFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EducationCreateSerializer
        elif self.action == 'update':
            return serializers.EducationUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        investor = selectors.investor_list().filter(user=request.user).last()
        services.education_create(user=investor, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.education_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)


class CompanyBalanceViewSet(viewsets.ModelViewSet):
    queryset = selectors.company_balance_list()
    serializer_class = serializers.CompanyBalanceOutSerializer
    http_method_names = ['get', 'post', 'head']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.company_balance_create(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)