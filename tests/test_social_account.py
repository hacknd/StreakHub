from django.utils.translation import ugettext_lazy as __
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from rest_framework import test, reverse
import httpretty
import json
import requests
import unittest
EPIC_JSON={
    "token": "487793df5d9fd76966a8ff1d3915e8035482597944a230355d44e0a92a52edee",
    "expiry": "2019-05-29T20:18:48.768478Z",
    "user": {
        "id": 2,
        "token": "487793df5d9fd76966a8ff1d3915e8035482597944a230355d44e0a92a52edee",
        "first_name": "",
        "last_name": "",
        "username": "_ber.ni.e_",
        "email": "benkaranja43@gmail.com",
        "is_email_active": False,
        "phone_number": "",
        "is_phone_active": False
    }
}
class AccountSocialAccountTest(test.APITestCase):
	def setUp(self):
		'''
		Setting up the new site for the new default application
		'''
		httpretty.enable()

	def _domain_information_pull_with_json(self, provider):
		return json.dumps(
			{
			"code":"oofgawd",
			"redirect_uri":(('http://{}{}').format(Site.objects.get_current().domain, reverse.reverse('account-social-login', args=(provider,)))).replace('example.com', 'localhost:8000'),
			"provider":provider
			}
			)

	def test_social_account_with_no_valid_provider(self):
		'''
		Testing the instance of a foreign backend
		'''
		provider='facebook'
		resp = self.client.get(reverse.reverse('account-social-login', args=(provider,)))
		self.assertEqual(resp.status_code, 500)
		self.assertEqual(resp.data['detail'], __('Missing Backend'))

	def test_social_account_for_discord(self):
		'''
		Testing instance for discord application
		'''	
		self.provider='discord'
		resp = self.client.get(reverse.reverse('account-social-login', args=(self.provider,)))
		self.assertEqual(resp.status_code, 302)	
		httpretty.register_uri(
			httpretty.GET,
			resp.url,
			body=self._domain_information_pull_with_json(self.provider),
			status=200
			)
		response=requests.get(resp.url)
		httpretty.register_uri(
			httpretty.POST,
			response.json()['redirect_uri'],
			body=EPIC_JSON,
			status=201
			)
		url=reverse.reverse('account-social-login', args=(self.provider,))	
		post_response = self.client.post( url, format='json')
		print(post_response)	
		self.assertEqual(post_response.status_code, 201)

	def tearDown(self):
		httpretty.disable()	