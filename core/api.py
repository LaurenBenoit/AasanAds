import base64
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from core.models import Locations,Ad
import json
from django.views.decorators.csrf import csrf_exempt



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
		ad_obj = Ad(title= title,description=data['description'],
					phone_number=data['phone_number'], address=address,
					link_url=link_url,image_url=image_url, button_label=button_label,
					contact_preference=contact_preference, only_ladies=only_ladies, app_code=app_code)

		ad_obj.full_clean()
		ad_obj.save()
		for lo in data['location']:
			l = Locations(ad=ad_obj, location=lo)
			l.save()
		return HttpResponse(ad_obj.id)
	return HttpResponse('description and phone_number not provided')

@csrf_exempt
def createAd(request,realm="", *args, **kwargs):
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
						print request.META.keys()
						print request.POST.keys()
						print request.body
						return process_createAd(request)
					else:
						return HttpResponse('Bad authentication')
				else:
					return HttpResponse('No such user')              	
	response = HttpResponse()
	response.status_code = 401
	response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
	return response


@csrf_exempt
def process_SMS(request,realm="", *args, **kwargs):
	print request.body
	msg = json.loads(request.body)
	dictz ={}
	diz = {'success' : True}
	# diz["task"] = 'send'
	# diz["messages"] =  [
	# 	{
	# 	"to": msg['from'],
	# 	"message": "Your message has been received!",
	# 	"uuid": "042c3515-ef6b-f424-c4qd"
	# 	}]
	dictz['payload'] = diz
	print dictz
	return JsonResponse(dictz)