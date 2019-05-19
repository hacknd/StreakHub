from django.urls import path
from client_auth import views


urlpatterns = [
	path('register/', views.AccountCreateView.as_view(), name='account-create'),
	path('login/', views.AccountLoginView.as_view(), name='account-login'),
	path('logout/',views.AccountLogoutView.as_view(), name='account-logout'),
	path('logoutall/', views.AccountLogoutAllView.as_view(), name='account-logoutall'),
	path('login/social/<provider>/',views.AccountSocialLoginView.as_view(), name='account-social-login'),
    ]