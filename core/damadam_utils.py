import core.models as coremodels
damadam_url = 'http://10.50.202.168:8000'
damadam_user = 'aasanads'
damadam_pass = 'damadam1234'
import json
import unirest

def sendAd(ad1, clicks, tid):
	print 'data'
	data = ad1.to_json()
	data['clicks'] = clicks
	data['tid'] = tid
	data = json.dumps(data)
	response = unirest.post(damadam_url + "/api/ad/live/", headers={ "Content-type": "application/json" },params=data,  auth=(damadam_user, damadam_pass))
	print response