import core.models as coremodels
damadam_url = 'http://10.50.202.168:8000'
damadam_user = 'aasanads'
damadam_pass = 'damadam1234'
import json
import unirest

def deleteTopup(tid, callback):
	data = {}
	data['tid'] = tid
	unirest.post(damadam_url + "/api/ad/delete/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=callback)
def resumeTopup(tid, callback):
	data = {}
	data['tid'] = tid
	unirest.post(damadam_url + "/api/ad/resume/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=callback)
def suspendTopup(tid, callback):
	data = {}
	data['tid'] = tid
	unirest.post(damadam_url + "/api/ad/suspend/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=callback)



def sendAd(ad1, clicks, tid):
	print 'data'
	data = ad1.to_json()
	data['clicks'] = clicks
	data['tid'] = tid
	data = json.dumps(data)
	response = unirest.post(damadam_url + "/api/ad/live/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=ad_sent_callback)
	print response

def ad_sent_callback(response):
	print response.body