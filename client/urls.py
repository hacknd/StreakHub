from django.urls import path, include
from client import views

urlpatterns = [
	path('', views.api_root, name='root'),
	
    ]

