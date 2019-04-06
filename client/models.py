from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="members")
	username= models.CharField(max_length=20,unique=True)
	full_name= models.CharField(max_length=20)
	email= models.EmailField()
	phone_regex= RegexValidator(regex=r'^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	bio = models.CharField(max_length=300)
	profile_pic = models.ImageField()
	cover_pic = models.ImageField()
	community = models.ManyToManyField(Community,  blank=True,related_name='community_member')
	tournament = models.ManyToManyField(Tournament, blank=True,related_name='tournament_member')
	bookmarks = models.ManyToManyField(Bookmarks, blank=True, related_name='bookmarks_member')
	following = models.ManyToManyField(Following, blank=True, related_name='following_member')
	followers = models.ManyToManyField(Followers, blank=True, related_name='followers_member')

	def __str__(self):
		return self.username

	class Meta:
		verbose_name_plural = "Members"	

	@receiver
	def create_member_profile(sender, instance, created, **kwargs):
		if created:
			Members.objects.create(user=instance)


	@receiver
	def save_user_profile(sender, instance, **kwargs):
		instance.members.save()

