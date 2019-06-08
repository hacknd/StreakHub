from django.db import models
from client_auth.utils import GamEngineException
from client.models import Follow

class FollowManager(models.Manager):	
	def followers(self, user):
		qs = Follow.objects.filter(followee=user).all()
		followers = [u.follower for u in qs]
		return followers

	def following(self, user):
		qs = Follow.objects.filter(follower=user).all()
		following = [u.followee for u in qs]
		return following

	def add_follower(self, follower, followee):
		if follower == followee:
			GamEngineException(code=400,detail=__('Impossible Action'))
		relation, created = Follow.objects.get_or_create(follower=follower, followee=followee)
		return relation

	def remove_follower(self, follower, followee):
		return 'string'