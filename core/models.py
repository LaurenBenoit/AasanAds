from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models


AD_STATUS = (
	(0, 'Unapproved'), # Not Running
	(1, 'Approved'), # Running.
	(2, 'Paused'), # Not Running
	(3, 'Running'), # Running.
	(4, 'Expired'), # Not Running
)

LOCATION = (
	(0, 'Karachi'), 
	(1, 'Rawalpindi'),
	(2, 'Islamabad'), 
	(3, 'Lahore'), 
	(4, 'Quetta'), 
	(5, 'Hyderabad'),
	(6, 'Multan'),
	(7, 'Sukkur'),
	(8, 'Gujrat'),
	(9, 'Peshawer'),
	(10, 'Sialkot'),
	(11, 'Faisalabad'),
	(12, 'Gujranwala'),
	(13, 'Wah'),
	(14, 'Sarghoda'),
	(15, 'Bahwalpur'),
	(16, 'Mardan'),
	(17, 'Abbottabad'),
	(18, 'Swat'),
	(19, 'Gilgit'),
	(20, 'Skardu'),
)


PREFERENCE = (
	(0, 'Call/Text'), 
	(1, 'Call'),
	(2, 'Text'),
) 



class Ad(models.Model):
	title = models.TextField()
	description = models.TextField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=20) # validators should be a list
	status = models.IntegerField(choices=AD_STATUS, default=0)
	location = models.IntegerField(choices=LOCATION, default=0)
	address = models.TextField()
	link_url = models.TextField()
	link_descriptor = models.TextField(default='click here!')
	contact_preference = models.IntegerField(choices=PREFERENCE, default=0)


# Create your models here.
