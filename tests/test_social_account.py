from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import test, reverse
from django.utils.translation import ugettext_lazy as __
import httpretty
from django.contrib.sites.models import Site
import json
import requests



class AccountSocialAccountTest(APITestCase):
	def setUp(self):
		'''
		Setting up the new site for the new default application
		'''
		httpretty.enable()
