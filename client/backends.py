from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import Permission
from rest_framework import authentication, exceptions, status
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as __
from .utils import GamEngineException400
from rest_framework import exceptions
from knox.auth import TokenAuthentication
Account = get_user_model()




class AuthBackend:
	"""
	Authentication......starts....now
	"""
	def authenticate(self, request, username=None, password=None, token=None , **kwargs):
		if username is None:
			username = kwargs.get(Account.USERNAME_FIELD)
		try:
			# If this is an email which is blank, he or she is unable to get in with a blakn username.
			if username == '':
				msg=__('Not permitted to do this request.')
				raise GamEngineException400(msg)
			# Try to fetch the account by search the username or email field
			account = Account.objects.get(Q(username=username)|Q(email=username)|Q(phone_number=username))
			if account.check_password(password):
				# print('AuthBackend Authentication in play.')
				return account
		except Account.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existign and a non existing existing user
			return None

		else:
			if account.check_password(password) and self.user_can_authenticate(user):
				return	account

	def get_user(self, user_id):
		try:
			account = Account.objects.get(pk=user_id)
			# print('AuthBackend Authentication in play.')
		except Account.DoesNotExist:
			return None
		return account if self.user_can_authenticate(account) else None 			


		
