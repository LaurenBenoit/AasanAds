import base64
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from core.models import LocationCounter,Ad

from django.views.decorators.csrf import csrf_exempt



def process_createAd(request):
	if 'description' in request.POST and 'phone_number' in request.POST:
		title = None
		address = None
		link_url = None
		image_url = None
		button_label = 'Yeh Dubao!'
		contact_preference = 0
		only_ladies = 0
		if 'title' in request.POST:
			title = request.POST['title']
		if 'address' in request.POST:
			address = request.POST['address']
		if 'link_url' in request.POST:
			link_url = request.POST['link_url']
		if 'image_url' in request.POST:
			image_url = request.POST['image_url']
		if 'button_label' in request.POST:
			button_label = request.POST['button_label']
		if 'contact_preference' in request.POST:
			contact_preference = request.POST['contact_preference']
		if 'only_ladies' in request.POST:
			only_ladies = request.POST['only_ladies']
		ad_obj = Ad(title= title,description=request.POST['description'],
					phone_number=request.POST['phone_number'], address=address,
					link_url=link_url,image_url=image_url, button_label=button_label,
					contact_preference=contact_preference, only_ladies=only_ladies)
		ad_obj.full_clean()
		ad_obj.save()
		return HttpResponse('saving...')
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

						return process_createAd(request)
					else:
						return HttpResponse('Bad authentication')
				else:
					return HttpResponse('No such user')              	
	response = HttpResponse()
	response.status_code = 401
	response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
	return response