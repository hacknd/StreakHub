from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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

class LoginUserSerializer(serializers.ModelSerializer):
	username = serializers.CharField(
		required=True,
		)	
	password = serializers.CharField(
		min_length=8,
		write_only=True
		)		

	def validate(self , data):
		account = authenticate(username=data['username'], password=data['password'])
		if account and account.is_active:
			return account
		raise serializers.ValidationError("Ooops! Wrong credentials, try again?")	

	class Meta:
		model = get_user_model()
		fields = ('username', 'password')	

class AuthTokenSerializer(serializers.ModelSerializer):
	class Meta:
		model = AuthToken
		fields = ('token')



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
	token=serializers.SerializerMethodField()
	password = serializers.CharField(write_only=True)

	def get_token(self, obj):
		jwt_payload_handler = __import__('rest_framework_jwt').settings.api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = __import__('rest_framework_jwt').settings.api_settings.JWT_ENCODE_HANDLER



		payload = jwt_payload_handler(obj)
		token = jwt_encode_handler(payload)
		return token

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

	class Meta:
		model = User
		fields = ('token', 'username', 'password',)		