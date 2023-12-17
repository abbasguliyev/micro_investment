from django.utils.translation import gettext_lazy as _
from rest_framework.views import Response
from rest_framework import status, viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend
from notification.api import selectors, serializers, filters


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = selectors.notification_list()
    serializer_class = serializers.NotificationOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NotificationFilter
    http_method_names=["get", "head"]