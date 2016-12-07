import core.models as coremodels
damadam_url = 'damadam.pk'
damadam_user = ''
damadam_pass = ''
import json
import unirest

def sendAd(ad1, clicks):
	print ad1.to_json()		
	unirest.get(damadam_url + "/api/saveLiveAd", headers={ "Accept": "application/json" },data=data)
	