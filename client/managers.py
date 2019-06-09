from django.db import models
from client.urls import urlpatterns
from client_auth.utils import GamEngineException
from django.utils.translation import ugettext_lazy as __

class FollowManager(models.Manager):	
	def followers(self, user):
		qs = self.model.objects.filter(followee=user).all()
		followers = [u.followers for u in qs]
		return followers

	def following(self, user):
		qs = self.model.objects.filter(followers=user).all()
		following = [u.followee for u in qs]
		return following

	def add_follower(self, followers, followee):
		if followers == followee:
			raise GamEngineException(code=400,detail=__('Impossible Action'))
		relation, created = self.model.objects.get_or_create(followers=followers, followee=followee)

		if created is False:
			raise GamEngineException(code=500, detail=__("User '%s' already follows '%s'" % (followers, followee)))
		return relation

	def remove_follower(self, followers, followee):
		try:
			qs = self.model.objects.get(followers=followers, followee=followee)
			qs.delete()
			return True
		except self.model.DoesNotExist:
			raise GamEngineException(code=301, detail=__('No Follow Relation'))			