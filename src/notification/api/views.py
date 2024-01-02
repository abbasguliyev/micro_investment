from django.utils.translation import gettext_lazy as _
from rest_framework.views import Response
from rest_framework import status, viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend
from notification.api import selectors, serializers, filters, services


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = selectors.notification_list()
    serializer_class = serializers.NotificationOutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NotificationFilter
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.NotificationUpdateSerializer
        elif self.action == 'update':
            return serializers.NotificationUpdateSerializer

        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            try:
                notf_count = selectors.notification_list().filter(user=serializer.data[0].get('user'), is_read=False).count()
            except:
                notf_count = 0

            return self.get_paginated_response({"notf_count": notf_count, "data": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        try:
            notf_count = selectors.notification_list().filter(user=serializer.data[0].get('user'), is_read=False).count()
        except:
            notf_count = 0
        return Response({"notf_count": notf_count, "data": serializer.data})


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.notification_all_read(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'detail': _("Ok")}, status=status.HTTP_201_CREATED,
                        headers=headers)
