from django.urls import path, include
from rest_framework import routers
from notification.api.views import NotificationViewSet

router = routers.DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
