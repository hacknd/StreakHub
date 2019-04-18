from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as __


class CustomAccountManager(BaseUserManager):
	"""
	Custom Account Model Manager used to show it suppose to do during account creation and superuser creation 
	"""
	def create_user(self,username, email , password, **extra_fields):
		'''
		Create and save an individual account with the given email and password
		'''

		if extra_fields.get('is_superuser') is True:
			email = None
			account = self.model(username=username, **extra_fields)
			account.set_password(password)
			account.save()
			return account
		if not email:
			raise ValueError(__('The Email must be set'))
		email = self.normalize_email(email)
		account = self.model(email=email, **extra_fields)
		account.set_password(password)
		account.save()
		return account 	

	def create_superuser(self, username, password, email=None, **extra_fields):
		'''
		Create and save a superuser account with username and password
		'''		
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(__('superuser must have is_staff=True'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(__('superuser must have is_superuser=True'))
		return self.create_user(username=username, email=None, password=password, **extra_fields)		