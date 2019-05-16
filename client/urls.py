from django.urls import path, include
from client import views

urlpatterns = [
	path('', views.api_root, name='root'),
	path('auth/register/', views.AccountCreateView.as_view(), name='account-create'),
	path('auth/login/', views.AccountLoginView.as_view(), name='account-login'),
	path('auth/logout/',views.AccountLogoutView.as_view(), name='account-logout'),
	path('auth/logoutall/', views.AccountLogoutAllView.as_view(), name='account-logoutall'),
	path('auth/login/social/<provider>/',views.AccountSocialLoginView.as_view(), name='account-social-login'),
    ]

