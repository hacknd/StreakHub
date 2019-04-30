from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import Permission
from rest_framework import authentication, exceptions
Account = get_user_model()


class AuthBackend(object):
	"""
	Authentication......starts....now
	"""
	def authenticate(self, request, username=None, password=None, token=None , **kwargs):
		if username is None:
			username = kwargs.get(Account.USERNAME_FIELD)
		try:
			# Try to fetch the account by search the username or email field
			account = Account.objects.get(Q(username=username)|Q(email=username)|Q(phone_number=username))
			if account.check_password(password):
				print('/llloooooof')
				return account
		except Account.DoesNotExist:
			# Run the default password hasher once toreduce the timing
			# difference between an existign and a non existing existing user
			return Account.set_password(self, raw_password=password)
		else:
			if account.check_password(password) and self.user_can_authenticate(user):
				return	account

	def get_user(self, user_id):
		try:
			account = Account.objects.get(pk=user_id)
		except Account.DoesNotExist:
			return None	
		return account if self.user_can_authenticate(account) else None 			

