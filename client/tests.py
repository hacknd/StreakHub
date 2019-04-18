from django.test import TestCase
from django.contrib.auth import get_user_model


Account = get_user_model()

# Create your tests here.
class AccountManagerTests(TestCase):
	def test_create_account_test(self):
		account = Account.objects.create_user(username='ben', email='normal@user.com', password='foo')
		self.assertEqual(account.email, 'normal@user.com')
		self.assertTrue(account.is_active)
		self.assertFalse(account.is_staff)
		self.assertFalse(account.is_superuser)


		with self.assertRaises(TypeError):
			Account.objects.create_user()
		with self.assertRaises(TypeError):
			Account.objects.create_user(email='')
		with self.assertRaises(ValueError):
			Account.objects.create_user(email='', password='foo')
