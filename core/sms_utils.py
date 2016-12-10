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

def parse_sms(sender, message):
	# if sender == '3737': # most import if condition to verify.
	if 1 == 1: # remove this line when upar wali condition activated.
		message = message.lower()
		print message
		if 'easypaisa' in message: # this is actually a easypaisa msg
			if 'with easypaisa account' in message and 'cnic' not in message: 
				# ACCOUNT TO ACCOUNT
				msg_list = message.split(' ')
				index = msg_list.index('received')
				index += 2
				money = float(msg_list[index])
				index = msg_list.index('from')
				index += 1
				name= []
				name.append(msg_list[index])
				if msg_list[index+1] != 'with':
					name.append(msg_list[index+1])
				if msg_list[index+2] != 'with':
					name.append(msg_list[index+2])
				if msg_list[index+3] != 'with':
					name.append(msg_list[index+3])
				index_of_num = message.find('03')
				number = message[index_of_num:index_of_num+12]
				
				print 'money'
				print money
				print 'name'
				print name
				print 'number'
				print number
			elif 'account' in message and 'cnic' not in message: 
				# CNIC TO WALLET
				pass
			elif 'account' not in message and 'cnic' in message:
				# CNIC TO CNIC
				msg_list = message.split(' ')
				trx_id = int(msg_list[2].replace(".",""))
				print 'trx_id'
				print trx_id
				money = float(msg_list[msg_list.index('rs.')+1])
				print 'money'
				print money

				cnic = msg_list[msg_list.index('cnic')+1]
				print 'cnic'
				print cnic
				pass

