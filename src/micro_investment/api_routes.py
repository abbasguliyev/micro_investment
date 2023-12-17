from django.urls import include, path

urlpatterns = [
    path('users/', include('account.api.urls')),
    path('entrepreneurs/', include('entrepreneur.api.urls')),
    path('investments/', include('investment.api.urls')),
    path('notifications/', include('notification.api.urls')),
]