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

class AccountCreate(APIView):
	"""
	Create an account from scratch
	"""
	def post(self, request, format='json'):
		serializer = AccountSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user=user)
				json = serializer.data
				json['token'] = token.key
				return Response(json,
					status=status.HTTP_201_CREATED
					)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
