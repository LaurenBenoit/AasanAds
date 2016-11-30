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
	address = models.TextField()
	link_url = models.TextField()
	link_descriptor = models.TextField(default='click here!')
	contact_preference = models.IntegerField(choices=PREFERENCE, default=0)
	submitted_time = models.DateTimeField(auto_now_add=True)
	total_money_paid = models.IntegerField(default=0)
	last_money_topup = models.IntegerField(default=0)
	#In order to get all topups call Ad.Topup_set.all()
	#In order to get all LocationCounter call Ad.LocationCounter_set.all()
	#https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_one/
	# see example r.article_set.all()
	def approve(self):
		self.status = 1
		self.save()

class Topup(models.Model):
	ad = models.ForeignKey(Ad)
	time = models.DateTimeField(auto_now_add=True)
	money_paid = models.IntegerField()
	is_running = models.BooleanField(default=True)
	expiry_time = models.DateTimeField()



class LocationCounter(models.Model):
	#https://docs.djangoproject.com/en/1.10/ref/models/options/#unique-together
	class Meta:
		unique_together = (('ad', 'location'),)
	ad = models.ForeignKey(Ad)
	location = models.IntegerField(choices=LOCATION, default=0)
	clicks = models.IntegerField(default=0)
# Create your models here.









#TODO feature: EDIT description, title, etc.
