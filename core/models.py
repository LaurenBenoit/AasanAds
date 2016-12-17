from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import json
import SMS_MESSAGES

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
	(6, 'Suspended'),		# Not Running
	(7, 'Stopped'),			# Not Running
	(8, 'SUNSET')
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



APP_CODE = (
	(0, 'all'),
	(1, 'damadam')
)

#Cool down time before SalesAgent can claim another ad
COOLDOWN_TIME = 2*60

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
	app_code = models.IntegerField(default=0)
	user_id = models.IntegerField(blank=True, null=True)
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
	def to_json(self):
		data = {}
		data['description'] = self.description
		data['phone_number'] = self.phone_number
		data['location'] = self.getLocations()
		data['only_ladies'] = self.only_ladies
		data['status'] = self.status
		data['contact_preference'] = self.contact_preference
		data['title'] = self.title
		data['address'] = self.address
		data['user_id'] = self.user_id
		return data
	def approve(self):
		self.status = 1
		self.save()

	def getLocations(self):
		locs = []
		for counterObject in self.locations_set.all():
			locs.append(counterObject.location)
		return locs


TOPUP_STATUS = (
	(0, 'awaiting_payment'),	#waiting for payment!
	(1, 'paid'),		#PAID and LIVE
	(2, 'free'), # THIS AD WAS an APPROVED AD AND ITS FREE.
	(3, 'expired'),		# expired. :(
	(4, 'suspended')
)

class Topup(models.Model):
	ad = models.ForeignKey(Ad)
	time = models.DateTimeField(auto_now_add=True)
	money_paid = models.IntegerField()
	status = models.IntegerField(choices=TOPUP_STATUS, default=0)
	expiry_time = models.DateTimeField(null=True, blank=True)
	clicks = models.IntegerField(default=0)
	total_clicks = models.IntegerField(default=0)
	total_impressions = models.IntegerField(default=0)
	closed_by = models.ForeignKey(SalesAgent, null=True, blank=True)
	cnic = models.CharField(null=True, blank=True,max_length=15)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+923334404403'.")
	phone_number = models.CharField(validators=[phone_regex], max_length=20) # validators should be a list
	
	def deleteCall(self, response):
		print 'deleted'
		self.delete()
	def suspendCall(self, response):
		print 'suspend'
		self.status = 4
		print response
	def resumeCall(self, response):
		print 'resummedd'
		if self.status == 4:
			if money_paid != 0:
				self.status = 1
			else:
				self.status = 2
		print response
	def resumeReq(self):

		# TODO
		if ad.app_code == 1:
			import damadam_utils
			damadam_utils.resumeTopup(self.id, self.resumeCall)	

		# import functools
	def suspend(self):
		if self.ad.app_code == 1:
			import damadam_utils
			damadam_utils.suspendTopup(self.id, self.suspendCall)
		# import functools
	def deleteReq(self):
		if ad.app_code == 1:
			import damadam_utils
			damadam_utils.deleteTopup(self.id, self.deleteCall)

	def make_it_live(self):
		locs = self.ad.getLocations()
		topuplocationcounters = []
		import sms_utils
		import redis_utils

		if self.ad.status == 4:
			self.ad.status = 5
		for loc in locs:
			topuplocationcounters.append(TopupLocationCounter(topup=self, location= loc))
		TopupLocationCounter.objects.bulk_create(topuplocationcounters)
		redis_utils.put_ad(self.ad, self.clicks, self.id)
		if self.status == 2:
			sms_utils.send_sms(self.phone_number, SMS_MESSAGES.ad_approved, self.ad)
		if self.status == 1:
			sms_utils.send_sms(self.phone_number, SMS_MESSAGES.ad_live, self.ad)

		if self.ad.app_code == 1:
			import damadam_utils
			damadam_utils.sendAd(self.ad,self.clicks, self.id)
		self.ad.save()
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
	impressions = models.IntegerField(default=0)
	clicks = models.IntegerField(default=0)



class SMSIncoming(models.Model):
	secret = models.CharField(max_length=20, null=True, blank=True)
	sender = models.CharField(max_length=20)
	sent_timestamp = models.DateTimeField(null=True, blank=True)
	time_recieved = models.DateTimeField(auto_now_add=True)
	device_id = models.CharField(max_length=20,null=True, blank=True)
	message = models.CharField(max_length=918,null=True, blank=True)

OUTGOING_STATUS = (
	(0, 'pending'),
	(1, 'sent')
)
OUTGOING_TYPE = (
	(0, 'ad_approved'),
	(1, 'free clicks expired'),
	(2, 'to agent_close_this_ad'),
	(3, 'ad_approved'),
	(4, 'iss number pai payment karein'),
	(5, 'payment ho gaye. khoofia code bhejein'),
	(6, 'to agent. khoofia code lein.'),
	(7, 'ad_is_live'),
	(8, 'itnay clicks reh gaye hain.'),
	(9, 'ad_expired. '),
	(10,'to agent. ad_expired'),
	(11,'Custom')
)

class SMSOutgoing(models.Model):
	ad = models.ForeignKey(Ad, null=True, blank=True)
	topup = models.ForeignKey(Topup, null=True, blank=True)
	type = models.IntegerField(choices= OUTGOING_TYPE)
	reciever = models.CharField(max_length=20)
	message = models.CharField(max_length=918,null=True, blank=True)
	status = models.IntegerField(choices=OUTGOING_STATUS, default=0)
	sent_timestamp = models.DateTimeField(auto_now_add=True)
	def resend(self):
		import sms_utils
		sms_utils.resend_sms(self)



TRANSACTION_STATUS = (
	(0, 'PENDING PAYMENT'),
	(1, 'PENDING KHOOFIA CODE'), # only cnic to cnic.
	(2, 'PAYMENT unverified'),
	(3, 'PAYMENT VERIFIED'),
	(4, 'PAYMENT IS LESS'),
	(5, 'Mismatched payment'),
	(6, 'PAYMENT IS MORE'),
)

PAISA_TYPES = (
	(0, 'easyPaisa'),	#Telenor
	(1, 'timePey'),		#Zong
	(2, 'uPay'),		#Ufone
	(3, 'jazzCash'),	#Jazz,mobilink
	(4,'mobilePaisa')	#Warid
)
class Transaction(models.Model):
	trx_id = models.IntegerField(null=True, blank=True)
	status = models.IntegerField(choices=TRANSACTION_STATUS, default = 0)
	paisa_type =models.IntegerField(choices=PAISA_TYPES, default=0)
	topup = models.ForeignKey(Topup, null = True, blank= True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+923334404403'.")
	phone_number = models.CharField(validators=[phone_regex], max_length=20, db_index=True)
	money = models.FloatField(null=True, blank=True)
	cnic = models.CharField(null=True, blank=True,max_length=15, db_index=True)
 	secret_code = models.CharField(null=True, blank= True, max_length=10)
 	sms = models.OneToOneField(SMSIncoming, blank=True, null=True)
