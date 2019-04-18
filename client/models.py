from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as __
from .managers import CustomAccountManager
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


	def __str__(self):
		return self.get_id_display()

class Account(AbstractUser):
	username = models.CharField(max_length=13, unique=True)
	email = models.EmailField(__('email address'), unique=True)
	is_email_active = models.BooleanField(default=False)
	is_phone_active = models.BooleanField(default=False)
	role = models.ManyToManyField('client.role',related_name='user_role')

	def initialize_default_role(self):
		for role_choice_id in [ 1 , 2 ]:
			roleModel = Role(id=role_choice_id)
			roleModel.save()
			self.role.add(roleModel)



	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = CustomAccountManager()

	def __str__(self):
		return self.email

class Member(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,related_name="members")
	username= models.CharField(max_length=20,unique=True)
	full_name= models.CharField(max_length=20)
	email= models.EmailField()
	phone_regex= RegexValidator(regex=r'^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	bio = models.CharField(max_length=300)
	profile_pic = models.ImageField()
	cover_pic = models.ImageField()
	community = models.ManyToManyField('client.community',  blank=True,related_name='community_member')
	tournament = models.ManyToManyField('client.tournament', blank=True,related_name='tournament_member')
	bookmarks = models.ManyToManyField('client.bookmarks', blank=True, related_name='bookmarks_member')
	following = models.ManyToManyField('client.following', blank=True, related_name='following_member')
	followers = models.ManyToManyField('client.followers', blank=True, related_name='followers_member')

	def __str__(self):
		return self.email

	class Meta:
		verbose_name_plural = "Members"	

	def save_user(self):
		self.save()

	@receiver(post_save, sender=get_user_model())
	def create_member_profile(sender, instance, created, **kwargs):
		if created:
			Member.objects.create(user=instance)


	@receiver(post_save, sender=get_user_model())
	def save_user_profile(sender, instance, **kwargs):
		instance.members.save()

	def setup_email_to_instance(self):
		self.user.email = self.email


class RegistrationAudit(models.Model):
	user_id=models.CharField(max_length=300,unique=True, default='1')
	session_id = models.CharField(max_length=300, unique=True, default='1')
	pass

	
	class Meta:
		verbose_name_plural = 'RegistrationAudits'




class Blog(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Blogs'

	def __str__(self):
		return self.names	


class Post(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Posts'

	def __str__(self):
		return self.names	

class Community(models.Model):
	name = models.CharField(max_length=200,default='ooof')
	
	class Meta:
		verbose_name_plural = 'Communities'

	def __str__(self):
		return self.name	
class Tournament(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Tournaments'

	def __str__(self):
		return self.names	
class Bookmarks(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Bookmarks'

	def __str__(self):
		return self.names

class Following(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Followings'

	def __str__(self):
		return self.names
class Followers(models.Model):
	names = models.CharField(max_length=200,default='ooof')

	class Meta:
		verbose_name_plural = 'Followers'

	def __str__(self):
		return self.names

