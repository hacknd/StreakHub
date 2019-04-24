# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import SessionAuthentication , BasicAuthentication
from rest_framework import status
from client.serializers import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


# Create your views here.

