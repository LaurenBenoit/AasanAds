from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


def get_SalesAgent(self):
	try:
		return self.salesagent
	except:
		return None
User.add_to_class("get_SalesAgent",get_SalesAgent)


AD_STATUS = (
	(0, 'Unapproved'),		# Not Running
	(1, 'Approved/Unpaid'),	# Running.
	(2, 'Paused'),			# Not Running - 
	(3, 'Claimed'),			# Not Running - Claimed by some specific Agent.
	(4, 'Closed'),			# Not Running - Awaiting Verification.
	(5, 'Running'),			# Running.
	(6, 'Stopped'),			# Not Running
	(7, 'Expired')
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

PAISA_TYPES = (
	(0, 'easyPaisa'),	#Telenor
	(1, 'timePey'),		#Zong
	(2, 'uPay'),		#Ufone
	(3, 'jazzCash'),	#Jazz,mobilink
	(4,'mobilePaisa')	#Warid
)

#Cool down time before SalesAgent can claim another ad
COOLDOWN_TIME = 5*60

class SalesAgent(models.Model):
	#https://docs.djangoproject.com/en/1.10/topics/db/examples/one_to_one/
	user = models.OneToOneField(User, unique=True, primary_key=True)
	
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=20) # validators should be a list

	location = models.IntegerField(choices=LOCATION, default=0)

	user_rating = models.FloatField(default=0.0)
	rating_count = models.IntegerField(default=0)
	total_claimed = models.IntegerField(default=0)
	total_closed = models.IntegerField(default=0)
	money_made = models.IntegerField(default=0)
	commission_owed = models.IntegerField(default=0)
	commission_paid = models.IntegerField(default=0)
	last_closing_time = models.DateTimeField(blank=True, null=True)
	# Sales Agent can claim one ad per COOLDOWN_TIME.
	last_ad_claim_time = models.DateTimeField(blank=True, null=True)
	
class Ad(models.Model):
	title = models.TextField(null=True,blank=True)
	description = models.TextField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=20) # validators should be a list
	address = models.TextField(null=True,blank=True)
	link_url = models.TextField(null=True,blank=True)
	image_url = models.TextField(null=True,blank=True)
	button_label = models.TextField(default='Yeh Dubao!')
	contact_preference = models.IntegerField(choices=PREFERENCE, default=0)
	only_ladies = models.BooleanField(default=False)
	# auto add fields
	status = models.IntegerField(choices=AD_STATUS, default=0)
	submitted_time = models.DateTimeField(auto_now_add=True)
	total_money_paid = models.IntegerField(default=0)
	last_money_topup = models.IntegerField(default=0)

	claimed_by = models.ForeignKey(SalesAgent, null=True, blank=True)
	#In order to get all topups call Ad.Topup_set.all()
	#In order to get all LocationCounter call Ad.LocationCounter_set.all()
	#https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_one/
	# see example r.article_set.all()
	def approve(self):
		self.status = 1
		self.save()

	def getLocations(self):
		locs = []
		for counterObject in self.locationcounter_set.all():
			locs.append(counterObject.location)
		return locs


TOPUP_STATUS = (
	(0, 'closed'),	#Telenor
	(1, 'paid'),		#Zong
	(2, 'expired')		#Ufone
)

class Topup(models.Model):
	paisa_type =models.IntegerField(choices=PAISA_TYPES, default=0)
	paisa_id = models.IntegerField(null=True, blank=True)
	ad = models.ForeignKey(Ad)
	time = models.DateTimeField(auto_now_add=True)
	money_paid = models.IntegerField()
	status = models.IntegerField(choices=TOPUP_STATUS, default=0)
	expiry_time = models.DateTimeField()
	clicks = models.IntegerField(default=0)
	closed_by = models.ForeignKey(SalesAgent, null=True, blank=True)


class Locations(models.Model):
	class Meta:
		unique_together = (('ad', 'location'),)
	ad = models.ForeignKey(Ad)
	location = models.IntegerField(choices=LOCATION)

class TopupLocationCounter(models.Model):
	#https://docs.djangoproject.com/en/1.10/ref/models/options/#unique-together
	class Meta:
		unique_together = (('topup', 'location'),)
	topup = models.ForeignKey(Topup)
	location = models.IntegerField(choices=LOCATION, default=0)
	clicks = models.IntegerField(default=0)


#TODO feature: EDIT description, title, etc.
