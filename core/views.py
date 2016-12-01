from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View,TemplateView
from django.views.generic.edit import CreateView
from core.models import LocationCounter,Ad
import redis_utils
import core.models as coremodels
import core.forms as coreforms
def Hello(request, **kwargs):
	return JsonResponse({'foo':'bar'})
# Create your views here.


def get_ad():
	pass

def is_Agent(user):
	return user.groups.filter(name='Agent').exists()

def adApprove(request, pk=None, *args, **kwargs):
	if is_Agent(request.user):
		Ad.objects.get(id=pk).approve()
		# TODO: ADD ad to REDIS.
	return redirect('sales_agent')

def adDelete(request, pk=None, *args, **kwargs):
	if is_Agent(request.user):
		Ad.objects.get(id=pk).delete()
	return redirect('sales_agent')


class SalesAgent(View):
	def get(self, request, *args, **kwargs):
		if is_Agent(request.user):
			unapproved_ads = Ad.objects.filter(status=0).all()
			approved_ads = Ad.objects.filter(status=1).all()
			# for ad in uapproved_ads:
			# 	pass
			data = {'unapproved_ads':unapproved_ads,'approved_ads':approved_ads}
			return render_to_response('SalesAgent.html', data)
		elif request.user.is_authenticated():
			return HttpResponse("u r not agent")
		else:
			return HttpResponse("plz login")

class AdCreateView(CreateView):
	form_class = coreforms.AdCreateForm
	template_name = 'form.html'
	def form_valid(self, form):
		self.object = form.save() # create the AD
		ad_locations = form.cleaned_data['location']
		for loc in ad_locations:
			loc_object = LocationCounter(ad=self.object, location=loc) # create location counters.
			# these are for tracking hits 
			loc_object.save()
		print self.object.locationcounter_set.all()
		return HttpResponse("saved!")

		