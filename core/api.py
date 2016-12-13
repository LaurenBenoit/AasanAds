import base64
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from core.models import Locations,Ad, SMSIncoming, Topup
import json
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
import datetime
import redis_utils
import sms_utils
import SMS_MESSAGES


def process_updateAd(request):
	data = json.loads(request.body)
	print data
	redis_utils.update_ad(data['tid'], data['ad_impressions'], data['ad_clicks'],
		data['impression_breakdown'], data['click_breakdown'])
	if data['ad_done'] == True:
		redis_utils.save_ad(data['tid'], True)
		redis_utils.delete_ad(data['tid'])
		# also send SMS here.

		return HttpResponse('ad updated, saved, expired, deleted')
	else:
		return HttpResponse('ad updated. :)')
	# TODO
def bulk_updateAd(request):
	list_data = json.loads(request.body)
	response = []
	for data in list_data:
		redis_utils.update_ad(data['tid'], data['ad_impressions'], data['ad_clicks'],
			data['impression_breakdown'], data['click_breakdown'])
		if data['ad_done'] == True:
			redis_utils.save_ad(data['tid'], True)
			redis_utils.delete_ad(data['tid'])
			# also send SMS here.
			response.append('ad updated, saved,expired, deleted')
		else:
			response.append('ad updated.')
	return JsonResponse(response)


def process_createAd(request):
	data = json.loads(request.body)
	if 'description' in data and 'phone_number' in data:
		title = None
		address = None
		link_url = None
		image_url = None
		button_label = 'Yeh Dubao!'
		contact_preference = 0
		only_ladies = 0
		app_code = 0
		print data
		if 'title' in data:
			title = data['title']
		if 'address' in data:
			address = data['address']
		if 'link_url' in data:
			link_url = data['link_url']
		if 'image_url' in data:
			image_url = data['image_url']
		if 'button_label' in data:
			button_label = data['button_label']
		if 'contact_preference' in data:
			contact_preference = data['contact_preference']
		if 'only_ladies' in data:
			only_ladies = data['only_ladies']
		if 'location' in data:
			locations = data['location']
		if 'app_code' in data:
			app_code = data['app_code']
		if 'app_code' in data:
			app_code = data['app_code']
		ad_obj = Ad(title= title,description=data['description'],
					phone_number=data['phone_number'], address=address,
					link_url=link_url,image_url=image_url, button_label=button_label,
					contact_preference=contact_preference, only_ladies=only_ladies, app_code=app_code)

		ad_obj.full_clean()
		ad_obj.save()
		loc_list = []
		for lo in data['location']:
			loc_list.append(Locations(ad=ad_obj, location=lo))
		Locations.objects.bulk_create(loc_list)
		return HttpResponse(ad_obj.id)
	return HttpResponse('description and phone_number not provided')

def process_auth(request):
	if 'HTTP_AUTHORIZATION' in request.META:
		auth = request.META['HTTP_AUTHORIZATION'].split()
		if len(auth) == 2:
			# NOTE: We are only support basic authentication for now.
			#
			if auth[0].lower() == "basic":
				uname, passwd = base64.b64decode(auth[1]).split(':')
				user = authenticate(username=uname, password=passwd)
				if user is not None:
					if user.is_superuser:
						return True
					else:
						return HttpResponse('Bad authentication')
				else:
					return HttpResponse('No such user')
	response = HttpResponse()
	response.status_code = 401
	response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
	return response

@csrf_exempt
def createAd(request,realm="", *args, **kwargs):
	auth_result = process_auth(request)
	if auth_result == True:
		return process_createAd(request)
	return auth_result

@csrf_exempt
def updateAd(request,realm="", *args, **kwargs):
	auth_result = process_auth(request)
	if auth_result == True:
		return process_updateAd(request)
	return auth_result


@csrf_exempt
def process_SMS(request,realm="", *args, **kwargs):		
		print "\n\n"
		sms_msg = json.loads(request.body)
		d_id = None
		if 'device_id' in sms_msg:
			d_id = sms_msg['device_id']
		time = None
		if 'sent_timestamp' in sms_msg:
			time = datetime.datetime.fromtimestamp(int(sms_msg['sent_timestamp'])/1000.0).replace(tzinfo=utc)
		sms = SMSIncoming(message=sms_msg['message'], sender= sms_msg['from'], secret=sms_msg['secret'],
			device_id=d_id, sent_timestamp=time)
		sms.save()
		sms_utils.parse_sms(sms_msg['from'], sms_msg['message'], sms)
		dictz ={}
		diz = {'success' : True}
		# diz["task"] = 'send'
		# diz["messages"] =  [
		# 	{
		# 	"to": '+923234837525',
		# 	"message": "Your message has been received!",
		# 	"uuid": "042p3515-ef6b-f424-c4qd"
		# 	}]
		dictz['payload'] = diz
		print dictz
		return JsonResponse(dictz)
