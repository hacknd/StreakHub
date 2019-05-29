# Django Packages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, login, signals

# Rest Framework Packages
from rest_framework import response, views, generics, status, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
# Installed Packages
from rest_social_auth.views import SocialKnoxUserAuthView
from knox.views import LoginView
from knox import settings, models, auth

# Local Packages
from .serializers import CreateAccountSerializer, SocialSerializer, AccountSerializer
from .utils import GamEngineRedirectAuthorizationBackend
"""
Local Variables
"""
current_format = None

# Create your views here.


class AccountCreateView(generics.GenericAPIView):
	"""
	Create an account from scratch
	"""
	queryset = get_user_model().objects.all()
	serializer_class = CreateAccountSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			if account:
				json = AccountSerializer(
					account,
					context=self.get_serializer_context()).data
				return response.Response(
					json,
					status=status.HTTP_201_CREATED, *args, **kwargs
					)
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, *args, **kwargs)	

class AccountLoginView(LoginView):
	"""
	Logging in a user that verification is required and a authorization header is created in the django api side
	"""
	permission_classes = (permissions.AllowAny, )
	def post(self, request, format=current_format):
		serializer = AuthTokenSerializer(
			data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.validated_data['user']
		login(request, account)
		json = super(AccountLoginView, self).post(
			request, format=current_format)
		token = json.data["token"]
		return response.Response(json.data, status=status.HTTP_201_CREATED, headers={'Authorization': 'Token {0}'.format(token)})


class AccountSocialLoginView(SocialKnoxUserAuthView):
	"""
	Logging in a user that social verification is required and a authorization header is created in the django api side
	"""
	serializer_class = SocialSerializer
	def get(self, request, provider, code=None, format=current_format):
		try:
			code = request.GET['code']
			data = GamEngineRedirectAuthorizationBackend(provider, code)
		except KeyError:
			return GamEngineRedirectAuthorizationBackend(provider, code)
		(request.data).update(data)
		return self.post(request, format=current_format)

	def post(self, request, format=current_format):
		json = super(AccountSocialLoginView, self).post(
			request, format=current_format)
		token = models.AuthToken.objects.get(
			token_key=json.data['token'][:settings.CONSTANTS.TOKEN_KEY_LENGTH])
		data = {
			"token": json.data['token'],
			"expiry": token.expiry
		}
		data["user"] = json.data
		login(request, token.user, backend='client.backends.AuthBackend')
		return response.Response(data, status=status.HTTP_201_CREATED, headers={'Authorization': 'Token {0}'.format(json.data['token'])})

class AccountLogoutAllView(views.APIView):
	'''
	Log the user out of all sessions 
	I.E delete all auth tokens for the user
	'''
	authentication_classes = (auth.TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, format=current_format, *args, **kwargs):
		request.user.auth_token_set.all().delete()
		signals.user_logged_out.send(sender=request.user.__class__,
							 request=request, user=request.user)
		return response.Response(None, status=status.HTTP_204_NO_CONTENT, *args, **kwargs)

class AccountLogoutView(views.APIView):
	"""
	Logging out a single device 
	closing a single sessions
	"""
	authentication_classes = (auth.TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, format=current_format, *args, **kwargs):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							 request=request, user=request.user, *args, **kwargs)
		return Response(None, status=status.HTTP_204_NO_CONTENT, *args, **kwargs)

class AccountLogoutView(views.APIView):
	"""
	Logging out a single device 
	closing a single sessions
	"""
	authentication_classes = (auth.TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, format=current_format, *args, **kwargs):
		request._auth.delete()
		signals.user_logged_out.send(sender=request.user.__class__,
							 request=request, user=request.user, *args, **kwargs)
		return response.Response(None, status=status.HTTP_204_NO_CONTENT, *args, **kwargs)

	def get(self, request, format=current_format, *args, **kwargs):
		return HttpResponseRedirect('/api/1.0', *args, **kwargs) 
