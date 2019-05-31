from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as __
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
from .managers import CustomAccountManager



class Account(AbstractUser):
	username = models.CharField(max_length=13, unique=True)
	email = models.EmailField(__('email address'))
	is_email_active = models.BooleanField(default=False)
	phone_regex = RegexValidator(
		regex=r'^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$',
		message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
		)
	phone_number = models.CharField(
		validators=[phone_regex],
		max_length=17,
		blank=True
		)
	is_phone_active = models.BooleanField(default=False)
	account_membership_id = models.CharField(
		max_length=20,
		unique=True,
		blank=True
		)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []
	
	objects = CustomAccountManager()

	@receiver(post_save, sender='client.Member')
	def account_membership_id(sender, instance, created, **kwargs):
		if created:
			pass


	def __str__(self):
		return self.username
class Role(models.Model):
	'''
	The Role Entries are managed in the system to decide who is who in the system

	'''
	ACCOUNT = 1
	INDIVIDUAL_ACCOUNT = 2
	TOURNAMENT_ADMIN = 3
	TOURNAMENT_SUPERVISOR = 4
	TOURNAMENT_FS = 5
	ADVERT_ACCOUNT = 6
	VERIFIED_ACCOUNT = 7

	ROLE_CHOICES = (
		(ACCOUNT, 'member'),
		(INDIVIDUAL_ACCOUNT, 'individual_account'),
		(TOURNAMENT_ADMIN, 'tournament_admin'),
		(TOURNAMENT_SUPERVISOR, 'tournament_supervisor'),
		(TOURNAMENT_FS, 'tournament_field_scorer'),
		(ADVERT_ACCOUNT, 'advertisement_account'),
		(VERIFIED_ACCOUNT, 'verified_account')
	)
	id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True, default=ACCOUNT)

	def save_role(self):
		self.save()

	def role_count(self):
		return len(self.ROLE_CHOICES)	
	def __str__(self):
		return self.get_id_display()