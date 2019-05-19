from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_social_auth.serializers import UserKnoxSerializer
from django.contrib.auth import get_user_model, authenticate, login
from knox.models import AuthToken

class CreateAccountSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=get_user_model().objects.all())]
		)
	username = serializers.CharField(
		required=True,
		max_length=32,
		validators=[UniqueValidator(queryset=get_user_model().objects.all())]
		)
	password = serializers.CharField(min_length=8, write_only=True)


	def create(self, validated_data):
		account = get_user_model().objects.create_user(username=validated_data['username'],email=validated_data['email'], password=validated_data['password'])
		return account

	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email', 'password')	

class AccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = get_user_model()
		fields = ('id','last_login','is_superuser','username','email','phone_number','is_active')		

class SocialSerializer(UserKnoxSerializer):
	def get_token(self, obj):
		
		from knox.models import AuthToken
		from knox.settings import knox_settings
		instance, token = AuthToken.objects.create(obj,knox_settings.TOKEN_TTL)
		
		return token

		


