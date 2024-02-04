from django.urls import path, include
from rest_framework import routers
from investment.api.views import InvestmentViewSet, InvestmentReportViewSet, AdminInvestmentViewSet

router = routers.DefaultRouter()
router.register(r'report', InvestmentReportViewSet, basename='investment_report')
router.register(r'admin-investments', AdminInvestmentViewSet, basename='admin_investment')
router.register(r'', InvestmentViewSet, basename='investment')

urlpatterns = [
    path('', include(router.urls)),
]
