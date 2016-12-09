import redis
import uuid
import json

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)

##########Redis Namespace##########

'''
#tid is topup ID

Active_location_ads
Set
la:{location_num}
name: "la:" + str(location) # la is location ads. These are sets that list active ads in each location.

Ad_total_click_counter
String
ac:{id}
name: "ac:" + str(tid). Will use increment on this number. Initially 0.

Ad_location_click_counter
String
al:{id}:{location_num}
name: "alc:" + str(tid) +":" + str(location). Will use increment on this number. Initially 0.

Ad_total_impressions_counter
String
ic:{id}
name: "ac:" + str(tid). Will use increment on this number. Initially 0.

Ad_location_impressions_counter
String
il:{id}:{location_num}
name: "alc:" + str(tid) +":" + str(location). Will use increment on this number. Initially 0.


Ad_Details
Hash
ad:{id}
name: "ad:" + str(tid)
{clicks, description, title, link_url, image_url,locations, button_label, contact_preference, address, only_ladies, status}
{cl, ds, ti, li, im, lo, bt, st, cp, ad, ol}




SMS_MODULE


SMS_SEND_QUEUE

LPUSH mylist "one"
LPUSH mylist "two"
LPUSH mylist "three"

RPOP mylist


'''

def put_ad(ad, clicks, tid):
	my_server = redis.Redis(connection_pool=POOL)
	pipeline1 = my_server.pipeline()
	
	# Add Ad_Details to redis.
	ad_mapping = {}
	ad_mapping['cl'] = clicks
	ad_mapping['ds'] = ad.description
	ad_mapping['ol'] = ad.only_ladies
	ad_mapping['cp'] = ad.contact_preference
	ad_mapping['lo'] = ad.getLocations()
	if ad.title is not None:
		ad_mapping['ti'] = ad.title
	if ad.link_url is not None:
		ad_mapping['li'] = ad.link_url
	if ad.image_url is not None:
		ad_mapping['im'] = ad.image_url
	if ad.button_label is not None:
		ad_mapping['bt'] = ad.button_label
	if ad.status is not None:
		ad_mapping['st'] = ad.status
	if ad.address is not None:
		ad_mapping['ad'] = ad.address
	pipeline1.hmset("ad:"+str(tid), ad_mapping)

	# Add Ad_total_click_counter
	pipeline1.set("ac:"+str(tid), "0")
	pipeline1.set("ic:"+str(tid), "0")
	# Add tid to Active_location_ads to redis.
	locs = ad.getLocations() # locs is location array.
	for loc in locs:
		pipeline1.sadd("la:"+str(loc), tid)

		# Add ad_location_click_counter
		pipeline1.set("al:"+str(tid)+":" +str(tid), "0")
		pipeline1.set("il:"+str(tid)+":" +str(tid), "0")
	pipeline1.execute()

def update_ad(tid, total_impressions, total_clicks, click_breakdown, impression_breakdown):
	my_server.set("ic"+str(tid), total_impressions)
	my_server.set("ac"+str(tid), total_clicks)
	locs = my_server.hget("ad:"+str(tid),"lo")
	locs = locs[1:-1]
	locs = locs.split(", ")
	for loc in locs:
		my_server.set("il:" +str(tid) +":"+str(loc), impression_breakdown[loc])
		my_server.set("al:" +str(tid) +":"+str(loc), click_breakdown[loc])



def save_ad(tid):
	


def delete_ad(tid):
	locs = my_server.hget("ad:"+ str(tid), "lo")
	locs = locs[1:-1]
	locs = locs.split(", ")
	for loc in locs:
		my_server.delete("il:" +str(tid) +":"+str(loc))
		my_server.delete("al:" +str(tid) +":"+str(loc))
		my_server.srem("la:" + str(loc), tid)	
	my_server.delete("ic" + str(tid))
	my_server.delete("ac" + str(tid))
	my_server.delete("ad" + str(tid))

def get_ad(location):
	pass