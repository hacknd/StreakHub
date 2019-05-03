from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect 
from rest_framework import status, generics, mixins
from client.serializers import *
from django.contrib.auth import get_user_model,login	
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions, reverse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.utils import timezone
from rest_framework.decorators import api_view
from knox.settings import knox_settings, CONSTANTS

current_format = None

@api_view(['GET'])
def api_root(request, format=current_format):
	if request.user.is_authenticated:
		data = {
		'ooh':'your alive',
		'user': AccountSerializer(request.user).data
		}
	else:
		# print(__import__('ipaddr').client_ip(request))
		# try:
		# 	real_ip = request.META['HTTP_X_FORWARDED_FOR']
		# 	print(real_ip)
		# 	regip = real_ip.split(",")[0]
		# except:
		# 	try:
		# 		regip = request.META['REMOTE_ADDR']
		# 	except:
		# 		regip = ""
		# print(regip)
		# if(regip == "127.0.0.1"):
		# 	myHost=__import__('socket').gethostname()
		# else:
		# 	resultHost = __import__('socket').gethostbyaddr(regip)
		# 	myHost=resultHost[0]
		# print(myHost)	
		if 'HTTP_X_FORWARDED_FOR' in request.META:
			print('yessss')
		else:
			print('damn')	
		import ipware as ip
		print(dir(ip))
		print(ip.get_client_ip(request))			
		data = {
		'ip':request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip(),
		'error': 'You saw this. You Killed It'
		}
	return Response(data, status=status.HTTP_200_OK)


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

	def get(self, request, format=None):
		print(request.user.is_active)
		print()
		return HttpResponseRedirect('/api/1.0')		


class AccountLoginAPI(LoginView):
	permission_classes = (permissions.AllowAny, )

	def post(self, request, format=None):
		serializer=AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		login(request, user)
		return super(AccountLoginAPI, self).post(request, format=None)


class AccountLogoutAllView(APIView):
	'''
	Log the user out of all sessions 
	I.E delete all auth tokens for the user
	'''

	authentication_classes = (TokenAuthentication, )
	# permission_classes = ( permissions.IsAuthenticated, )


	def post(self, request):
		request.user.auth_token_set.all().delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None, status=status.HTTP_204_NO_CONTENT)

	
	def get(self, request, format=None):
		print(request.user.is_active)
		print()
		return HttpResponseRedirect('/api/1.0')


class AccountLogoutView(APIView):
	authentication_classes = (TokenAuthentication, )
	# permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, format=None):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							request=request, user=request.user)
		return Response(None , status=status.HTTP_204_NO_CONTENT)

	def get(self, request, format=None):
		print(request.user.is_active)
		print()
		return HttpResponseRedirect('/api/1.0')
