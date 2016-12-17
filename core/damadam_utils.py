import core.models as coremodels
damadam_url = 'http://apollo7788.pagekite.me'
damadam_user = 'aasanads'
damadam_pass = 'damadam1234'
import json
import unirest

def deleteTopup(tid, callback):
	data = {}
	data['tid'] = topup.id
	data = json.dumps(data)
	unirest.post(damadam_url + "/api/ad/delete/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=callback)
def resumeTopup(tid, callback):
	data = {}
	data['tid'] = topup.id
	data = json.dumps(data)
	unirest.post(damadam_url + "/api/ad/resume/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass), callback=callback)
def suspendTopup(topup, callback):
	data = {}
	data['tid'] = topup.id
	data = json.dumps(data)
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