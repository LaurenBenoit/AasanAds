import core.views as coreviews
import core.api as coreapi
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^dashboard/$', login_required(coreviews.Dashboard.as_view()), name='sales_agent'),
	url(r'^dashboard/login/?$', coreviews.entrance),
	url(r'^dashboard/logout/?$', login_required(coreviews.logout_view)),
	
	url(r'^superuser/$', login_required(coreviews.Superuser.as_view()), name='super_user'),
	url(r'^superuser/createSalesAgent$', login_required(coreviews.SalesAgentCreateView.as_view())),
	url(r'^superuser/allAds$', login_required(coreviews.AllAds.as_view())),
	url(r'^superuser/resendSMS/(?P<pk>\d+)$', login_required(coreviews.resendSMS)),
	url(r'^superuser/topup/suspend/(?P<pk>\d+)$', login_required(coreviews.suspendTopupAd)),

	url(r'^$', coreviews.Hello),
	url(r'^ad/create/$', coreviews.AdCreateView.as_view()),
	url(r'^ad/delete/(?P<pk>\d+)$', coreviews.adDelete),
	url(r'^ad/update/(?P<pk>\d+)$', coreviews.AdUpdateView.as_view()),
	url(r'^ad/approve/(?P<pk>\d+)$', coreviews.adApprove),
	url(r'^ad/claim/(?P<pk>\d+)$', coreviews.adClaim),
	url(r'^ad/close/(?P<pk>\d+)$', coreviews.AdCloseView.as_view()),
	url(r'^ad/sunset/(?P<pk>\d+)$', coreviews.adSunset),
	url(r'^topup/khoofia/(?P<pk>\d+)$', coreviews.PutKhoofia.as_view()),



	url(r'^api/ad/send_sms/$', coreapi.sendSMS),
	url(r'^api/ad/create/$', coreapi.createAd),
	url(r'^api/postSMS/$', coreapi.process_SMS),
	url(r'^api/ad/update/$', coreapi.updateAd),

	
]