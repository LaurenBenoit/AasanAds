import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)

##########Redis Namespace##########

'''
Active_location_ads
Set
la:{location_num}
name: "la:" + str(location) # la is location ads. These are sets that list active ads in each location.

Ad_total_click_counter
String
ac:{id}
name: "ac:" + str(ad_id). Will use increment on this number. Initially 0.

Ad_location_click_counter
String
al:{id}:{location_num}
name: "alc:" + str(ad_id) +":" + str(location). Will use increment on this number. Initially 0.

Ad_total_impressions_counter
String
ic:{id}
name: "ac:" + str(ad_id). Will use increment on this number. Initially 0.

Ad_location_impressions_counter
String
il:{id}:{location_num}
name: "alc:" + str(ad_id) +":" + str(location). Will use increment on this number. Initially 0.


Ad_Details
Hash
ad:{id}
name: "ad:" + str(ad_id)
{clicks, description, title, link_url, image_url, button_label, status}
{cl, ds, ti, li, im, bt, st}
'''

def put_ad(ad, clicks):
	my_server = redis.Redis(connection_pool=POOL)
	pipeline1 = my_server.pipeline()
	
	# Add Ad_Details to redis.
	ad_mapping = {}
	ad_mapping['cl'] = clicks
	ad_mapping['ds'] = ad.description
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
	pipeline1.hmset("ad:"+str(ad.id), ad_mapping)

	# Add Ad_total_click_counter
	pipeline1.set("ac:"+str(ad.id), "0")
	pipeline1.set("ic:"+str(ad.id), "0")
	# Add ad_id to Active_location_ads to redis.
	locs = ad.getLocations() # locs is location array.
	for loc in locs:
		pipeline1.sadd("la:"+str(loc), ad.id)

		# Add ad_location_click_counter
		pipeline1.set("al:"+str(ad.id)+":" +str(loc), "0")
		pipeline1.set("il:"+str(ad.id)+":" +str(loc), "0")

	pipeline1.execute()
	

def get_ad(location):
	pass