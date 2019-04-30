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
from rest_framework  import authentication , permissions
from rest_framework.decorators import api_view
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
	
# 	queryset=get_user_model()
# 	serializer_class=LoginUserSerializer

# 	def post(self, request, *args , **kwargs):
# 		serializer = self.get_serializer(data=request.data)
# 		if serializer.is_valid():
# 			account = serializer.validated_data
# 			if account:
# 				token = AuthToken.objects.create(account)[1]
# 				json=AccountSerializer(account, context=self.get_serializer_context()).data
# 				json['token'] = token
# 				return Response(json,
# 					status=status.HTTP_201_CREATED
# 					)
# 			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
User = get_user_model()


@api_view(['GET'])
def current_user(request):
	"""
	Determining the current user by their token

	"""

	serializer = UserSerializer(request.user)
	return Response(serializer.data)


class UserListJWT(APIView):
	"""
	Creating a user
	"""

	permission_classes = (permissions.AllowAny, )


class AccountLogoutView(APIView):
	authentication_classes = (TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, format=None):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None, status=status.HTTP_204_NO_CONTENT) 
