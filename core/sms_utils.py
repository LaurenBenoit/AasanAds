import unirest
from core.models import SMSOutgoing
import functools
import urllib
SMS_URL= 'http://shahz.pagekite.me/sendsms'
def send_sms(to, message):
	# to phone number must be in URI. for some reason unirest does not decode it!
	unirest.get(SMS_URL, params = {'phone':urllib.pathname2url(to), 'text':message}, callback = functools.partial(callback, to, message))

def callback(to, message, response):
	print 'response'
	print response.body
	print 'to'
	print to
	print 'message'
	print message
	status = 0
	if 'SENT!' in response.body:
		status = 1
	sms = SMSOutgoing(reciever=to, message=message,status = status)
	sms.save()