from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from client_auth.models import Role

class Member(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,related_name="user_members")
	username= models.CharField(max_length=20,unique=True)
	is_admin = models.BooleanField(default=False)
	full_name= models.CharField(max_length=20)
	email= models.EmailField()
	phone_number = models.CharField(max_length=17, blank=True)
	bio = models.CharField(max_length=300)
	profile_pic = models.ImageField()
	cover_pic = models.ImageField()
	community = models.ManyToManyField('client.Community',  blank=True,related_name='community_member')
	tournament = models.ManyToManyField('client.Tournament', blank=True,related_name='tournament_member')
	bookmarks = models.ManyToManyField('client.Bookmarks', blank=True, related_name='bookmarks_member')
	following = models.ManyToManyField('client.Following', blank=True, related_name='following_member')
	followers = models.ManyToManyField('client.Followers', blank=True, related_name='followers_member')
	roles = models.ManyToManyField('client_auth.Role',related_name='user_role')


	def initialize_default_role(user):
		for role_choice_id in [ 1, 2 ]:
				roleModel = Role.objects.get(id=role_choice_id)
				user.roles.add(roleModel)
	class Meta:
		verbose_name_plural = "Members"	

	def save_user(self):
		self.save()

	@receiver(pre_save, sender=get_user_model())
	def create_roles(sender, instance, **kwargs):
			for ids in range(0, Role.role_count(Role)+1):
				if Role.objects.count() >= Role.role_count(Role):
					pass
				else:
					role=Role.objects.create(id= ids)
					role.save_role()

	@receiver(post_save, sender=get_user_model())
	def create_member_account(sender, instance, created, **kwargs):
		if created:
			if instance.is_superuser == True:
				Member.objects.create(user=instance, username=instance.username, email=instance.email, is_admin=True, phone_number=instance.phone_number)
				Member.initialize_default_role(Member.objects.get(user=instance))
			else:		
				Member.objects.create(user=instance, username=instance.username, email=instance.email, phone_number=instance.phone_number)
				Member.initialize_default_role(Member.objects.get(user=instance))
		
	@receiver(post_save, sender=get_user_model())
	def save_member_account(sender, instance, **kwargs):
		instance.user_members.save()
		
	def __str__(self):
		return self.user.username 


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

