from django.db import models
from django.core.validators import RegexValidator

	
class Members(models.Model):
	username= models.CharField(max_length=20,unique=True)
	full_name= models.CharField(max_length=20)
	email= models.EmailField()
	phone_regex= RegexValidator(regex=r'^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	bio = models.CharField(max_length=300)
	profile_pic = models.ImageField()
	cover_pic = models.ImageField()
