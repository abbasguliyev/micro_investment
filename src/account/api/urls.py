from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from account.api.views import UserViewSet, ExperienceViewSet, EducationViewSet, LoginView, CompanyBalanceViewSet

router = routers.DefaultRouter()
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'company-balance', CompanyBalanceViewSet, basename='company_balance')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('', include(router.urls)),
]
