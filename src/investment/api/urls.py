from django.urls import path, include
from rest_framework import routers
from investment.api.views import InvestmentViewSet

router = routers.DefaultRouter()
router.register(r'', InvestmentViewSet, basename='investment')

urlpatterns = [
    path('', include(router.urls)),
]
