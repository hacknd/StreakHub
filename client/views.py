from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from client.serializers import *
from django.contrib.auth import get_user_model	
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from django.contrib.auth.signals import user_logged_out
from django.utils import timezone


@api_view(['GET'])
def current_user(request):
	"""
	Determining the current user by their token

	"""

	serializer = UserSerializer(request.user)
	return Response(serializer.data)


class AccountCreateAPI(generics.GenericAPIView):
	"""
	Create an account from scratch
	"""
	queryset=get_user_model().objects.all()
	serializer_class=CreateAccountSerializer


	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			if account:
				json = AccountSerializer(account, context=self.get_serializer_context()).data
				return Response(json,
					status=status.HTTP_201_CREATED
					)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountLoginAPI(LoginView):
	authentication_classes = [BasicAuthentication, ]


	def get(self, request, *args, **kwargs):
		return Response(AccountSerializer(request.user).data)

	def post(self, request, format=None):
		token_limit_per_user = self.get_token_limit_per_user()
		if token_limit_per_user is not None:
			now = timezone.now()
			token = request.user.auth_token_set.filter(expiry__gt=now)
			if token.count() >= token_limit_per_user:
				return Response(
					{"error": "Maximum amount of tokens allowed per user exceeded."},
					status=status.HTTP_403_FORBIDDEN
					)
		token_ttl = self.get_token_ttl()
		instance, token = __import__('knox').models.AuthToken.objects.create(request.user, token_ttl)
		user_logged_in.send(sender=request.user.__class__,
							request=request, 
							user=request.user	
							)				
		UserSerializer = LoginUserSerializer

		data = {
			'expiry': instance.expiry,
			'token': token
		}

		if UserSerializer is not None:
			data['user'] = UserSerializer(
				request.user,
				context=self.get_context()
				).data
		return Response(data)	


class AccountLogoutAllView(APIView):
	'''
	Log the user out of all sessions 
	I.E delete all auth tokens for the user
	'''

	authentication_classes = (TokenAuthentication, )
	permission_classes = ( permissions.IsAuthenticated, )


	def post(self, request):
		request.user.auth_token_set.all().delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None, status=status.HTTP_204_NO_CONTENT)

	
	def get(self, request):
		return Response({'status': 'No User'}, status=status.HTTP_200_OK)



class AccountLogoutView(APIView):
	authentication_classes = (TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, format=None):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None, status=status.HTTP_204_NO_CONTENT) 

