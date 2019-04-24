from django.urls import path
from client import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('auth/register/', views.AccountCreateAPI.as_view(), name='account-create'),
	path('auth/login/', views.AccountLoginAPI.as_view(), name='account-login')
]