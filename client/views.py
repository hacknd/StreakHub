from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.http import HttpResponseRedirect 
from django.contrib.auth import get_user_model,login	
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins, permissions, reverse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from knox.views import LoginView
from knox.auth import TokenAuthentication
from knox.settings import knox_settings, CONSTANTS
from client.serializers import CreateAccountSerializer,AccountSerializer

current_format = None

@api_view(['GET'])
def api_root(request, format=current_format, *args,**kwargs):
	authentication_classes = (TokenAuthentication, )
	permission_classes = ( permissions.IsAuthenticated, )

	if request.user.is_authenticated:data = {'ooh':'your alive','user': AccountSerializer(request.user).data}
	else:data = {'error': 'You saw this. You Killed It'}
	return Response(data, status=status.HTTP_200_OK, *args,**kwargs)


class AccountCreateView(generics.GenericAPIView):
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
					status=status.HTTP_201_CREATED, *args,**kwargs
					)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,*args,**kwargs)

	def get(self, request, format=current_format,*args,**kwargs):
		print(request.user.is_active)
		print()
		return HttpResponseRedirect('/api/1.0')		


class AccountLoginView(LoginView):
	"""
	Logging in a user that verification is required and a authorization header is created in the django api side
	"""
	permission_classes = (permissions.AllowAny, )

	def post(self, request, format=current_format):
		serializer=AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.validated_data['user']
		login(request, account)
		json = super(AccountLoginView, self).post(request, format=current_format)
		token = json.data["token"]
		return Response(json.data, status=status.HTTP_201_CREATED, headers={'Authorization':'Token {0}'.format(token)})

class AccountSocialLoginView(SocialKnoxUserAuthView):
	serializer_class = SocialSerializer

	def post(self, request, format=current_format):
		json = super(AccountSocialLoginView, self).post(request, format=current_format)
		token = __import__('knox').models.AuthToken.objects.get(token_key=json.data['token'][:__import__('knox').settings.CONSTANTS.TOKEN_KEY_LENGTH])

		data = {
			"token":json.data['token'],
			"expiry":token.expiry
		}
		data["user"] = json.data
		return Response(data, status=status.HTTP_201_CREATED)
class AccountLogoutAllView(APIView):
	'''
	Log the user out of all sessions 
	I.E delete all auth tokens for the user
	'''
	authentication_classes = (TokenAuthentication, )
	permission_classes = ( permissions.IsAuthenticated, )


	def post(self, request ,format=current_format, *args, **kwargs):
		request.user.auth_token_set.all().delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None, status=status.HTTP_204_NO_CONTENT,*args,**kwargs)

	
	# def get(self, request, format=current_format, *args,**kwargs):
	# 	print(request.user.is_active)
	# 	print()
	# 	return HttpResponseRedirect('/api/1.0',*args,**kwargs)


class AccountLogoutView(APIView):
	"""
	Logging out a single device 
	closing a single sessions
	"""
	authentication_classes = (TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, format=current_format, *args,**kwargs):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user, *args,**kwargs)
		return Response(None , status=status.HTTP_204_NO_CONTENT, *args,**kwargs)

	def get(self, request, format=current_format, *args,**kwargs):
		print(request.user.is_active)
		print()
		return HttpResponseRedirect('/api/1.0', *args,**kwargs)
