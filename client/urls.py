from django.urls import path
from client import views
# from rest_framework.authtoken.views import obtain_auth_token

# from knox import views as knox_views


urlpatterns = [
	path('current_user/', views.current_user),
	path('users/', views.UserListJWT.as_view()),
	path('auth/register/', views.AccountCreateAPI.as_view(), name='account-create'),
	# path('auth/login/', views.AccountLoginAPI.as_view(), name='account-login'),
	]