from django.urls import path
from client import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('hello/', views.HelloView.as_view(), name='Hello' ),
	path('api-token-auth/',obtain_auth_token, name='api_token_auth'),
	path('example/', views.ExampleView.as_view(), name='example')
]