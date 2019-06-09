from rest_framework import test
from client.models import Member, Follow
from django.contrib.auth import get_user_model
from client_auth.utils import GamEngineException
from django.utils.translation import ugettext_lazy as __
Account = get_user_model()

class FollowSysTests(test.APITestCase):
	def setUp(self):
		self.test_user_1 = Account.objects.create_user(username='testuser1', email='test1@example.com',password='testpassword')
		self.test_user_2 = Account.objects.create_user(username='testuser2', email='test2@example.com',password='testpassword')
		self.member_1 = Member.objects.get(username=self.test_user_1.username)
		self.member_2 = Member.objects.get(username=self.test_user_2.username)

	def test_check_if_members_exist(self):
		'''
		Creating this test for users to be verified to be in the ailias database
		'''
		self.assertEqual(Member.objects.count(), 2)	
		self.assertEqual(Member.objects.get(id=1).username, self.test_user_1.username)
		self.assertEqual(Member.objects.get(id=2).username, self.test_user_2.username)
		self.assertEqual(Member.objects.get(id=1).email, self.test_user_1.email)
		self.assertEqual(Member.objects.get(id=2).email, self.test_user_2.email)
		

	def test_add_follower_testuser1_with_testuser2(self):	
		'''
		Testing the adding of the account members in the system.
		'''
		new_test_follow = Follow.objects.add_follower(self.member_1, self.member_2)
		self.assertEqual(new_test_follow.id, Follow.objects.count())
		self.assertEqual(new_test_follow.followers, self.member_1)
		self.assertTrue(self.member_1 in Follow.objects.followers(self.member_2))
		self.assertTrue(self.member_2 in Follow.objects.following(self.member_1))
		self.assertFalse(self.member_2 in Follow.objects.followers(self.member_1))
		self.assertFalse(self.member_1 in Follow.objects.following(self.member_2))

	def test_remove_follower_testuser1_with_testuser2(self):
		'''
		Testing the adding and deleting of the account members in the system.
		'''
		new_test_add_follow = Follow.objects.add_follower(self.member_1, self.member_2)
		self.assertEqual(new_test_add_follow.id, Follow.objects.count())
		self.assertEqual(new_test_add_follow.followers, self.member_1)
		self.assertTrue(self.member_1 in Follow.objects.followers(self.member_2))
		self.assertTrue(self.member_2 in Follow.objects.following(self.member_1))
		self.assertFalse(self.member_2 in Follow.objects.followers(self.member_1))
		self.assertFalse(self.member_1 in Follow.objects.following(self.member_2))
		new_test_remove_follow = Follow.objects.remove_follower(self.member_1, self.member_2)
		self.assertEqual(Follow.objects.count(), 0)

	def test_preventing_duplicate_follow_instances(self):
		'''
		Testing an instance where the user can follow and doesn't 
		'''		
		new_test_follow = Follow.objects.add_follower(self.member_1, self.member_2)
		self.assertEqual(new_test_follow.id, Follow.objects.count())
		self.assertEqual(new_test_follow.followers, self.member_1)
		self.assertTrue(self.member_1 in Follow.objects.followers(self.member_2))
		self.assertTrue(self.member_2 in Follow.objects.following(self.member_1))
		self.assertFalse(self.member_2 in Follow.objects.followers(self.member_1))
		self.assertFalse(self.member_1 in Follow.objects.following(self.member_2))
		new_test_follow_2 = Follow.objects.add_follower(self.member_1, self.member_2)
		self.assertRaises(GamEngineException, new_test_follow_2, detail=__("User '%s' already follows '%s'" % (followers, followee)))

	def tearDown(self):
		self.test_user_1.delete()
		self.test_user_2.delete()
		self.member_1.delete()
		self.member_2.delete()
