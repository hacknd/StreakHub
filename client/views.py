# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import SessionAuthentication , BasicAuthentication
from rest_framework import status, generics, mixins
from client.serializers import *
from django.contrib.auth import get_user_model, login
# from rest_framework.authtoken.models import Token
from knox.models import AuthToken
from rest_framework  import authentication 
# from knox.views import 

class AccountCreateAPI(generics.GenericAPIView):
	"""
	Create an account from scratch
	"""
	queryset=get_user_model()
	serializer_class=CreateAccountSerializer


	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			if account:
				custom_token=AuthToken.objects.create(account)[0]
				token= custom_token
				json = AccountSerializer(account, context=self.get_serializer_context()).data
				json['token'] = token
				return Response(json,
					status=status.HTTP_201_CREATED
					)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			
		
# class AccountLoginAPI(generics.GenericAPIView):
# 	"""
# 	Log in an account to the system
# 	"""
	
	queryset=get_user_model()
	serializer_class=LoginUserSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication


class AccountLoginAPI(KnoxLoginView):
	
	authentication_classes = [BasicAuthentication]
	# permission_classes = (permissions.AllowAny, )

	# def post(self, request, format=None):
	# 	serializer = AuthTokenSerializer
	# 	serialize.is_valid(raise_exception=True)
	# 	account = serializer.validated_data['user']
	# 	login(request, account)
	# 	return super(AccountLoginAPI, self).post(request, format='json')


	def post(self, request, *args , **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			account = serializer.validated_data
			if account:
				token = AuthToken.objects.create(account)[1]
				json=AccountSerializer(account, context=self.get_serializer_context()).data
				json['token'] = token
				return Response(json,
					status=status.HTTP_201_CREATED
					)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
				
