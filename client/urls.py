from django.urls import path
from client import views
# from rest_framework.authtoken.views import obtain_auth_token

from knox import views as knox_views


urlpatterns = [
	path('auth/register/', views.AccountCreateAPI.as_view(), name='account-create'),
	path('auth/login/', views.AccountLoginAPI.as_view(), name='account-login'),
	path('auth/logout/',knox_views.LogoutView.as_view(), name='knox_logout'),
	path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]