# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication , BasicAuthentication
# import unicode
# Create your views here.

class HelloView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		content = {'message': 'Hello World'}
		return Response(content)


class ExampleView(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes= (IsAuthenticated,)

	#		
	def get(selt, request, format=None):
		content = {
			'user': str(request.user),
			'auth': str(request.auth),

		}

		return Response(content)