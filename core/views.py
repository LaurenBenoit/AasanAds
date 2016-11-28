from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from core.models import Ad
def Hello(request, **kwargs):
	return JsonResponse({'foo':'bar'})
# Create your views here.


def approve_ad(ad):
	# add ad to redis.
	# convert ad status to approved.

def get_ad():
