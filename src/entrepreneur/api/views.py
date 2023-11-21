from django.utils.translation import gettext_lazy as _
from rest_framework.views import Response
from rest_framework import status, viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend

from entrepreneur.api import serializers, selectors, services, filters
from account.api.selectors import investor_list


class EntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = selectors.entrepreneur_list()
    serializer_class = serializers.EntrepreneurOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.EntrepreneurFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EntrepreneurCreateSerializer
        elif self.action == 'update':
            return serializers.EntrepreneurUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        investor = investor_list().filter(user=request.user).last()
        entrepreneur_data = services.entrepreneur_create(owner=investor, **serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response({"id": entrepreneur_data.id, "project_name": entrepreneur_data.project_name}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.entrepreneur_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)


class EntrepreneurImagesViewSet(viewsets.ModelViewSet):
    queryset = selectors.entrepreneur_images_list()
    serializer_class = serializers.EntrepreneurImagesOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.EntrepreneurImagesFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EntrepreneurImagesCreateSerializer
        elif self.action == 'update':
            return serializers.EntrepreneurImagesUpdateSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.entrepreneur_images_create(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.entrepreneur_images_update(instance=instance, **serializer.validated_data)
        return Response(data={'detail': _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)
