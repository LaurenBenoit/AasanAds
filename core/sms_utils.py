import unirest
from core.models import SMSOutgoing
from core.models import Transaction
import functools
import urllib
import SMS_MESSAGES
import re
SMS_URL= 'http://shahz.pagekite.me/sendsms'
def resend_sms(sms):
	unirest.get(SMS_URL, params = {'phone':urllib.pathname2url(sms.reciever), 'text':sms.message}, callback = functools.partial(callback_resend, sms))

def callback_resend(sms, response):
	print response.body
	if 'SENT!' in response.body:
		sms.status = 1
	sms.save()

def send_sms(to, message, ad):
	# to phone number must be in URI. for some reason unirest does not decode it!
	unirest.get(SMS_URL, params = {'phone':urllib.pathname2url(to), 'text':message}, callback = functools.partial(callback, to, message, ad))

def callback(to, message,ad, response):
	print 'response'
	print response.body
	print 'to'
	print to
	print 'message'
	print message
	status = 0
	if 'SENT!' in response.body:
		status = 1
	sms = SMSOutgoing(reciever=to, message=message,status = status, topup=None, type= 11, ad =ad)
	sms.save()

def parse_sms(sender, message, smsincoming):
	if sender == '+923404902633': # most import if condition to verify.
	# if 1 == 1: # remove this line when upar wali condition activated.
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
				print 'dsds'
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
				# LOOKUP CNIC TO topup.cnic
				n = Transaction.objects.filter(cnic=cnic, status=0).count()
				if n == 1:
					trc= Transaction.objects.get(cnic=cnic, status=0)
					trc.money = money
					trc.trx_id = trx_id
					trc.sms = smsincoming
					if trc.money >= trc.topup.money_paid:
						trc.status = 1
						if trc.money > trc.topup.money_paid:
							trc.status = 6
						trc.save()
						send_sms(trc.phone_number, SMS_MESSAGES.ask_secret_code_advertiser, trc.topup.ad)
						send_sms(trc.topup.closed_by.phone_number, SMS_MESSAGES.ask_secret_code_agent, trc.topup.ad)

					elif trc.money < trc.topup.money_paid: 
						Transaction(cnic= trc.cnic, status= 4, phone_number= trc.phone_number,
							trx_id=trx_id,topup=trc.topup,money=money,sms=smsincoming).save()

				else:
					print 'mismatched payment'
					Transaction(money=money, trx_id=trx_id,cnic=cnic,sms=smsincoming, status= 5).save()
					#  MAKE MISMATCHED PAYMENT here.
					pass
			else:
				print 'some thing happened'
	elif sender != '3737' and 2 == 2:
		sender = '0'+sender[3:]
		print sender
		khoofia = re.search('(\[^0-9])*\d{5}(\[^0-9])*',message,re.DEBUG)
		n = Transaction.objects.filter(phone_number= sender, status=1).count()
		print n
		if n == 1 and khoofia is not None:
			trc= Transaction.objects.get(phone_number= sender, status=1)
			trc.secret_code = khoofia
			print 'khoofia'
			print trc.secret_code
			trc.status = 2
			trc.save()
			trc.topup.make_it_live()
		else:
			print 'dsds'
			# THIS IS A RANDOM NUMBER. SENDING US 
			# TODO.
			pass
