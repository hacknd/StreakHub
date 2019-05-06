from django.test import TestCase
from django.contrib.auth import get_user_model
from client.models import Member
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
# from rest_framework.authtoken.models import Token
from knox.models import AuthToken as Token
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
			Account.objects.create_user(username='',email='', password='foo')

	def test_create_superuser(self):
		admin_account = Account.objects.create_superuser(username='super',password='foo',email='')
		admin_member = Member.objects.get(user=admin_account)
		self.assertEqual(admin_account.username, 'super')
		self.assertTrue(admin_account.is_active)
		self.assertTrue(admin_account.is_staff)
		self.assertTrue(admin_account.is_superuser)
		self.assertTrue(admin_member.is_admin)
		self.assertEqual(admin_account.username, admin_member.username)
		self.assertEqual(admin_account.phone_number, admin_member.phone_number)

		# print(type(admin_account.email))
		self.assertEqual(len(admin_account.email), 0)
		with self.assertRaises(ValueError):
			Account.objects.create_superuser(
				username='super', email='',password='foo', is_superuser=False
				)




class AccountsCreationTest(APITestCase):
	def setUp(self):
		
		# Originally creating a user from scratch to add up to users at the same time
		self.test_user = Account.objects.create_user(username='testuser', email='test@example.com',password='testpassword')
		
		#Url for creating an account
		self.create_url = reverse('account-create')

	def test_create_account(self):
		"""
		Ensure we can create a new account and a valid token is created with it  
		"""	
		data = {
			'username': 'foobar',
			'email': 'foobar@example.com',
			'password': 'somepassword',
		}

		response = self.client.post(self.create_url, data, format='json')
		user = Account.objects.latest('id')
		#We want to make sure we have two users in the database
		self.assertEqual(Account.objects.count(), 2)
		#And that we're returned a  201 created code
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		# Additionally, we want to return the username and email successful creation
		self.assertEqual(response.data['username'], data['username'])
		self.assertEqual(response.data['email'], data['email'])	

	
	def test_create_account_with_short_password(self):
		"""
		Ensure user is not created for password length less than 8
		"""
		data = {
			'username':'foobar',
			'password':'foo',
			'email':'foobarbaz@example.com',
		}

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['password']), 1)


	def test_create_account_with_no_password(self):
		data = {
			'username': 'foobar',
			'email': 'foobarbaz@example.com',
			'password': ''
		}		

		response = self.client.post(self.create_url , data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['password']), 1)


	def test_create_account_with_long_username(self):
		foo = 'foo'*30
		data = {
			'username': foo, 
			'email': 'foobarbaz@example.com',
			'password':'foobar',
		}	
		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['username']), 1)


	def test_create_account_with_no_username(self):
		data = {
			'username': '',
			'email': 'foobarbaz@example.com',
			'password':'foobar'
		}
		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['username']), 1)	


	def test_create_account_with_preexisting_username(self):
		data = {
			'username':'testuser',
			'email': 'username@example.com',
			'password':'testuser'
		}
		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['username']), 1)	

	def test_create_account_with_preexisting_email(self):
		data = {
			'username': 'testuser2',
			'email': 'test@example.com',
			'password': 'testuser'
		}

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['email']), 1)	

	def test_create_account_with_invalid_email(self):
		data = {
			'username': 'foobarbaz',
			'email': 'testing',
			'password': 'foobarbaz',
		}	
		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['email']), 1)

	def test_user_with_no_email(self):
		data = {
			'username': 'foobar',
			'email': '',
			'password':'foobarbaz'
		}	

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Account.objects.count(), 1)
		self.assertEqual(len(response.data['email']), 1)
		



class AccountLoginTest(APITestCase):
	def setUp(self):
		# Originally creating a user from scratch to add up to users at the same time
		self.test_user = Account.objects.create_user(username='testuser', email='test@example.com',password='testpassword',phone_number='+254715943570')
		self.token_test_user = Token.objects.create(user=self.test_user)[1]
		#Url for creating an account
		self.create_url = reverse('account-login')


	def test_authenticate_account_with_username(self):
		"""
		Ensuring the user is in the system and does the spot yaamean I was listening to reggae writing affi man
		"""	
		account = Account.objects.latest('id')
		token = Token.objects.create(account)[1]
		data = {
		'username':'testuser',
		'password':'testpassword',
		'token': token
		}	

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.data['token'], self.token_test_user.key)
		self.assertEqual(response.data['username'],data['username'])
		self.assertTrue(account.check_password(data['password']))
		self.assertEqual(Account.objects.count(), 1)

	def test_authenticate_account_with_email(self):
		"""
		Ensuring the user is in the system and does the activatian with email yaaa mean is a plan
		"""	
		data = {
			'username':'test@example.com',
			'password':'testpassword',
			'token':self.token_test_user,
		}

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(response.data['token'], self.token_test_user.key)
		self.assertEqual(response.data['email'],data['username'])
		self.assertTrue(account.check_password(data['password']))
		self.assertEqual(Account.objects.count(), 1)




		