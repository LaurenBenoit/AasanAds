from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import View,TemplateView
from django.views.generic.edit import CreateView, UpdateView
from core.models import Locations,Ad, Topup, TopupLocationCounter, Transaction
import redis_utils
import core.models as coremodels
import core.forms as coreforms
import django.contrib.auth
from django.contrib.auth.models import User
from sitegate.decorators import redirect_signedin, sitegate_view
import datetime
from django.utils import timezone
import redis_utils
import damadam_utils 
import sms_utils
import SMS_MESSAGES
def Hello(request, **kwargs):
	return JsonResponse({'foo':'bar'})
# Create your views here.


def get_ad():
	pass

def is_Agent(user):
	return user.groups.filter(name='Agent').exists()

def adApprove(request, pk=None, *args, **kwargs):
	if request.user.get_SalesAgent() is not None:
		ad1 = Ad.objects.get(id=pk)
		ad1.approve()
		clicks = 5
		topup = Topup(ad = ad1,money_paid=0, status=2, clicks=clicks, 
			closed_by=request.user.get_SalesAgent(), phone_number=ad1.phone_number)
		topup.save()
		topup.make_it_live()
		
		# put ad to my own redis.
		
		# TODO: ADD ad to REDIS.
	return redirect('sales_agent')

def adDelete(request, pk=None, *args, **kwargs):
	if request.user.get_SalesAgent() is not None:
		Ad.objects.get(id=pk).delete()
	return redirect('sales_agent')

def adClaim(request, pk=None, *args, **kwargs):
	agent = request.user.get_SalesAgent()
	if agent is not None:
		ad_claimed = Ad.objects.get(id=pk)
		ad_claimed.claimed_by = agent
		ad_claimed.status = 3
		ad_claimed.save()
		agent.last_ad_claim_time = datetime.datetime.now()
		agent.save()
	return redirect('sales_agent')

class Dashboard(View):
	def get(self, request, *args, **kwargs):
		if request.user.get_SalesAgent() is not None:
			unapproved_ads = Ad.objects.filter(status=0).all()
			approved_ads = Ad.objects.filter(status=1).all()
			paused_ads = Ad.objects.filter(status=2).all()
			agent = request.user.get_SalesAgent()
			my_claimed_ads = Ad.objects.filter(status=3, claimed_by=agent).all()
			# for ad in uapproved_ads:
			# 	pass
			can_claim = False
			if agent.last_ad_claim_time is None:
				can_claim = True
			else:
				timediff = timezone.now()- agent.last_ad_claim_time
				print timediff
				if timediff.seconds > coremodels.COOLDOWN_TIME:
					can_claim = True
			data = {'unapproved_ads':unapproved_ads,'approved_ads':approved_ads,
					'paused_ads':paused_ads,'timediff': timediff, 'can_claim': can_claim, 
					'my_claimed_ads':my_claimed_ads}
			return render_to_response('SalesAgent.html', data)
		elif request.user.is_superuser:
			return redirect('super_user')
		elif request.user.is_authenticated():
			return HttpResponse("u r not admin/agent")
		else:
			return HttpResponse("plz login")

class SalesAgentCreateView(CreateView):
	form_class = coreforms.AgentCreateForm
	template_name = 'form.html'
	def get_context_data(self,**kwargs):
		if self.request.user.is_superuser:
			return super(SalesAgentCreateView,self).get_context_data(**kwargs)
		else:
			return HttpResponse('BRO dnt hack my website')
	def form_valid(self, form):
		self.object = form.save(commit=False)
		#BILAL:WHY AM I DOING THIS?
		#BECAUSE otherwise the raw password gets saved and the authenticationdoesnt work.
		self.object.set_password(form.cleaned_data["password"])
		self.object.save()
		#----------
		agent = coremodels.SalesAgent(user=self.object)
		agent.location = form.cleaned_data["location"]
		agent.phone_number = form.cleaned_data['phone_number']
		agent.save()
		return redirect('super_user')
class Superuser(View):
	def get(self, request, *args, **kwargs):
		data = {}
		return render_to_response('admin.html', data)


class AdUpdateView(UpdateView):
	form_class = coreforms.AdUpdateForm
	model = coremodels.Ad
	template_name = 'form.html'
	def get_initial(self):
		variables = super(AdUpdateView, self).get_initial()
		variables['location'] = self.object.getLocations()
		return variables
	def form_valid(self, form):
		# this ssaves the ad fields.
		self.object = form.save()
		# This saves the Location field. Copied from Ad Create view form_valid
		ad_locations = form.cleaned_data['location']
		  # [ do_something(x) for x in a_list_of_objects ]
		loc_ids = self.object.locations_set.all().values_list('id',flat=True)
		Locations.objects.filter(id__in= loc_ids).delete()
		for loc in ad_locations:
			loc_object = Locations(ad=self.object, location=loc) # create location counters.
			# these are for tracking hits 
			loc_object.save()
		return redirect('sales_agent')
class AdCloseView(UpdateView):
	form_class = coreforms.AdCloseForm

	# fields = ['title', 'description', 'address', 'link_url', 'button_label', 'contact_preference']
	model = coremodels.Ad
	template_name = 'form.html'
	def get_initial(self):
		variables = super(AdCloseView, self).get_initial()
		variables['location'] = self.object.getLocations()
		return variables
	def form_valid(self, form):
		# this ssaves the ad fields.
		self.object = form.save()
		# This saves the Location field. Copied from Ad Create view form_valid
		ad_locations = form.cleaned_data['location']
		old_locs = self.object.locations_set.all()

		# deleting old locations
		for old_loc in old_locs:
			old_loc.delete()
		# adding new locations
		for loc in ad_locations:
			loc_object = Locations(ad=self.object, location=loc) # create location counters.
			# these are for tracking hits 
			loc_object.save()
		#Saving a TopUp
		topup = coremodels.Topup(closed_by = self.request.user.get_SalesAgent(), ad = self.object,
						clicks = form.cleaned_data['clicks_promised'],
						cnic = form.cleaned_data['cnic'],
						money_paid = form.cleaned_data['money_negotiated'],
						phone_number = form.cleaned_data['phone_number']
						)
		topup.save()
		Transaction(status=0, topup=topup, phone_number=form.cleaned_data['phone_number'],
			cnic=form.cleaned_data['cnic'])
		topuplocationcounters = []
		for loc in ad_locations:
			topuplocationcounters.append(TopupLocationCounter(topup=topup, location= loc))
		TopupLocationCounter.objects.bulk_create(topuplocationcounters)
		self.object.status = 4
		self.object.save()
		return redirect('sales_agent')

class AdCreateView(CreateView):
	form_class = coreforms.AdCreateForm
	template_name = 'form.html'
	# template_name = 'kunden/kunde_update.html'
	success_url = '/'
	def form_valid(self, form):
		self.object = form.save() # create the AD
		ad_locations = form.cleaned_data['location']
		for loc in ad_locations:
			loc_object = Locations(ad=self.object, location=loc) # create location counters.
			# these are for tracking hits 
			loc_object.save()
		return HttpResponse("saved!")

		
@sitegate_view(redirect_to='/dashboard',widget_attrs={'class': 'form-control', 'placeholder': lambda f: f.label}, template='form_bootstrap3') # This also prevents logged in users from accessing our sign in/sign up page.
def entrance(request):
	return render(request, 'entrance.html', {'title': 'Sign in & Sign up'})

def logout_view(request):
  django.contrib.auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/?logout=successful")
