from django.urls import path, include
from client import views
from knox import views as knox_views


urlpatterns = [
	path('', views.api_root, name='root'),
	path('auth/register/', views.AccountCreateAPI.as_view(), name='account-create'),
	path('auth/login/', views.AccountLoginAPI.as_view(), name='account-login'),
	path('auth/logout/',views.AccountLogoutView.as_view(), name='knox_logout'),
	path('auth/logoutall/', views.AccountLogoutAllView.as_view(), name='knox_logoutall'),
]

