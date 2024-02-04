from django.utils.translation import gettext_lazy as _
from rest_framework.views import Response
from rest_framework import status, viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend

from investment.api import serializers, selectors, services, filters
from investment.models import Investment
from account.api.selectors import investor_list


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = selectors.investment_list()
    serializer_class = serializers.InvestmentOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.InvestmentFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.InvestmentCreateSerializer
        elif self.action == 'update':
            return serializers.InvestmentUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        investor = investor_list().filter(user=request.user).last()
        services.investment_create(request_user=investor, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("İnvestisiyanız qeydə alındı")}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.investment_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        services.investment_delete(instance=instance)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_204_NO_CONTENT)


class AdminInvestmentViewSet(viewsets.ModelViewSet):
    queryset = selectors.admin_investment_list()
    serializer_class = serializers.InvestmentOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.InvestmentFilter
    pagination_class = None


class InvestmentReportViewSet(viewsets.ModelViewSet):
    queryset = selectors.investment_report_list()
    serializer_class = serializers.InvestmentReportOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.InvestmentReportFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.InvestmentReportCreateSerializer
        elif self.action == 'update':
            return serializers.InvestmentReportUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.investment_report_create(request_user=request.user, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Hesabatınız qeydə alındı")}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.investment_report_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)
