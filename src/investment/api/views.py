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
    http_method_names = ['get', 'post', 'head']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.InvestmentCreateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        investor = investor_list().filter(user=request.user).last()
        services.investment_create(investor=investor, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Investment successfully created")}, status=status.HTTP_201_CREATED, headers=headers)