from django.urls import path
from client import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('api/users/', views.UserCreate.as_view(), name='account-create'),
]