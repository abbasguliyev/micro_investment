from django.urls import path, include
from rest_framework import routers
from entrepreneur.api.views import EntrepreneurViewSet, EntrepreneurImagesViewSet

router = routers.DefaultRouter()
router.register(r'images', EntrepreneurImagesViewSet, basename='entrepreneur_image')
router.register(r'', EntrepreneurViewSet, basename='entrepreneur')

urlpatterns = [
    path('', include(router.urls)),
]
