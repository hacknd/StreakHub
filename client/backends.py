from django.contrib.auth import get_user_model
# from django.contrib.auth.models import check_password
from django.db.models import Q


Account = get_user_model()


class AuthBackend(object):
	"""
	Authentication......starts....now
	"""
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			if email == '':
				return None
			# Try to fetch the account by search the username or email field
			user = Account.objects.get(Q(username=username)|Q(email=username)|Q(phone_number=username))
			if user.check_password(password):
				return user
		except Account.DoesNotExist:
			# Run the default password hasher once toreduce the timing
			# difference between an existign and a non existing existing user
			Account.set_password(password)
