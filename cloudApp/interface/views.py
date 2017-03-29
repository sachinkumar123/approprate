from django.http import HttpResponse , StreamingHttpResponse
from django.shortcuts import render
from django.core import serializers
import time, math
from .models import Market, Item, LocalMarketData
from decimal import Decimal
import sys

# to CSRF exempt 
from django.views.decorators.csrf import csrf_exempt

try:
    from django.utils import simplejson as json
except ImportError:
	import json

def get_euclidean_dist(x1,y1,x2,y2):
	return pow((pow(x1-x2,2)+pow(y1-y2,2)), 0.5)

def get_distance_between_coordinates(lat1, lat2, long1, long2):
	"""
	Returns the distance in KM between two coordinates using haversine formula
	
	Args:
	    lat1 (Decimal): latitude of first coordinate
	    lat2 (Decimal): latitude of second coordinate
	    long1 (Decimal): longitude of first coordinate
	    long2 (Decimal): longitude of second coordinate

	Returns:
	    Float: Distance between two coordinates
	"""
	R = 6371 #Radius of Earth in KM
	dlong = abs(long2 - long1)
	dlat = abs(lat2 - lat1)
	a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlong/2))**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c
	return d

def home(request):
	return HttpResponse("<h1>Interface Home</h1>")

@csrf_exempt
def get_market_data_by_name(request):
    """Summary
    
    Args:
        request (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    if request.method == "POST":
		if 'name' in request.POST.keys():
			if request.POST['name']:
				name = request.POST['name']
				market_data = list(LocalMarketData.objects.filter(market_id__market_name=name))

				market_items = []

				for item in market_data:
					market_items.append({
											'item': item.item_id.item_name,
											'price': item.price,
											'item-image': item.item_id.item_image_url
										})

				market_items = json.dumps(market_items)
				return HttpResponse(market_items, content_type = 'application/json')
			else:
				return HttpResponse("argument name is not defined")
		else:
			return HttpResponse("Market name is necessary argument")
    else:
		return HttpResponse("Only POST request is accepted")

@csrf_exempt
def get_regional_markets_having_item(request):
	"""
		Returns the list of all markets which are having given item

	Args:
	    request (HttpRequest): HTTP Request coming from client's device. Expected to contain
	    POST request with following parameters -
	    region: String
	    item: String

	Returns:
	    HttpResponse: Response will be in JSON format containing list of details of Market. If
	    request is found to be malformed then appropriate response will be sent as error message.
	"""
	if request.method == "POST":
		if 'region' in request.POST.keys() and 'item' in request.POST.keys():
			if request.POST['region'] and request.POST['item']:
				region = request.POST['region']
				item = request.POST['item']
				markets = list(Market.objects.filter(localmarketdata__item_id__item_name = item, region = region))

				regional_markets = []

				for market in markets:
					regional_markets.append({'id': market.market_id,
											'name': market.market_name,
											'region': market.region,
											'state': market.state})

				regional_markets = json.dumps(regional_markets)
				return HttpResponse(regional_markets, content_type = 'application/json')
			else:
				return HttpResponse("argument isn't defined")
		else:
			return HttpResponse("region and item is necessary argument")
	else:
		return HttpResponse("Only POST request is accepted")

@csrf_exempt
def get_markets_in_region(request):
	"""
		Returns the list of all markets which are present in a given region
	
	Args:
	    request (HttpRequest): HTTP Request coming from client's device. Expected to contain
	    POST request with following parameters -
	    region: String
	
	Returns:
	    HttpResponse: Response will be in JSON format containing list of details of Market. If
	    request is found to be malformed then appropriate response will be sent as error message.
	"""
	if request.method == "POST":
		if 'region' in request.POST.keys():
			if request.POST['region']:
				region = request.POST['region']
				markets = list(Market.objects.filter(region = region))

				regional_markets = []

				for market in markets:
					regional_markets.append({'id': market.market_id,
											'name': market.market_name,
											'region': market.region,
											'state': market.state})

				regional_markets = json.dumps(regional_markets)
				return HttpResponse(regional_markets, content_type = 'application/json')
			else:
				return HttpResponse("argument isn't defined")
		else:
			return HttpResponse("region in the argument is necessary")
	else:
		return HttpResponse("Only POST request is accepted")

@csrf_exempt
def get_nearby_markets(request):
	"""
		Returns the list of all markets which are in vicinity of current location
	
	Args:
	    request (HttpRequest): HTTP Request coming from client's device. Expected to contain
	    POST request with following parameters -
	    latitude: Decimal
	    longitude: Decimal
	
	Returns:
	    HttpResponse: Response will be in JSON format containing list of details of Market. If
	    request is found to be malformed then appropriate response will be sent as error message.
	"""
	if request.method == "POST":
		if 'latitude' in request.POST.keys() and 'longitude' in request.POST.keys():
			if request.POST['latitude'] and request.POST['longitude']:
				THRESHOLD = 20000 #We take radius of 50KM to gather nearby markets
				markets = list(Market.objects.all())
				latitude = float(request.POST['latitude'])
				longitude = float(request.POST['longitude'])
				regional_markets = []

				for market in markets:
					print(get_distance_between_coordinates(latitude, float(market.latitude), longitude, float(market.longitude)))
					if get_distance_between_coordinates(latitude, float(market.latitude), longitude, float(market.longitude)) < THRESHOLD:
						regional_markets.append({'id': market.market_id,
												'name': market.market_name,
												'region': market.region,
												'state': market.state})

				regional_markets = json.dumps(regional_markets)
				return HttpResponse(regional_markets, content_type = 'application/json')
			else:
				return HttpResponse("arguments aren't defined")
		else:
			return HttpResponse("latitude and longitude arguments necessary in request")
	else:
		return HttpResponse("Only POST request is accepted")

@csrf_exempt
def get_closest_market(request):
	"""
		Returns the market which has minimum euclidean distance with the given latitude and longitude

	Args:
	    request (HttpRequest): HTTP Request coming from client's device. Expected to contain
	    POST request with following parameters -
	    latitude: Decimal
	    longitude: Decimal
	
	Returns:
	    HttpResponse: Response will be in JSON format containing details of Market. If
	    request is found to be malformed then appropriate response will be sent as error message.
	"""
	if request.method == "POST":
		if 'latitude' in request.POST.keys() and 'longitude' in request.POST.keys():
			if request.POST['latitude'] and request.POST['longitude']:
				markets = list(Market.objects.all())
				latitude = float(request.POST['latitude'])
				longitude = float(request.POST['longitude'])
				min_dist = sys.maxsize

				closest_market = min(markets, key = lambda market: 
					get_euclidean_dist(latitude, longitude, float(market.latitude), float(market.longitude))
									)

				closest_market = json.dumps({'id': closest_market.market_id,
											'name': closest_market.market_name,
											'region': closest_market.region,
											'state': closest_market.state})

				return HttpResponse(closest_market, content_type = 'application/json')
			else:
				return HttpResponse("arguments aren't defined")
		else:
			return HttpResponse("latitude and longitude arguments are necessary in request")

	else:
		return HttpResponse("Only POST request is accepted")
