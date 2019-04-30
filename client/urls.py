from django.urls import path
from client import views

urlpatterns = [
	path('current_user/', views.current_user),
	path('auth/register/', views.AccountCreateAPI.as_view(), name='account-create'),
	path('auth/login/', views.AccountLoginAPI.as_view(), name='account-login'),
	path('auth/logout/',views.AccountLogoutView.as_view(), name='knox_logout'),
	path('auth/logoutall/', views.AccountLogoutAllView.as_view(), name='knox_logoutall'),
]

