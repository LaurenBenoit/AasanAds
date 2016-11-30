import core.views as coreviews
from django.conf.urls import url

urlpatterns = [
	url(r'^$', coreviews.Hello),
	url(r'^dashboard/$', coreviews.SalesAgent.as_view(), name='sales_agent'),
	url(r'^ad/create/$', coreviews.AdCreateView.as_view()),
	url(r'^ad/delete/(?P<pk>\d+)$', coreviews.adDelete),
	url(r'^ad/approve/(?P<pk>\d+)$', coreviews.adApprove)

]