from django.db import models
from .managers import AccountTicketNumberManager
# Create your models here.
class AccountTicketNumber(models.Model):
	objects = AccountTicketNumberManager()
	pass