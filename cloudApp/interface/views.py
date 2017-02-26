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

def get_dist(x1,y1,x2,y2):	
	return pow((pow(x1-x2,2)+pow(y1-y2,2)), 0.5)

def home(request):
	return HttpResponse("<h1>Home</h1>")

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
		pass
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
				return HttpResponse("arguments aren't defined")
		else:
			return HttpResponse("latitude and longitude arguments necessary in request")
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
		pass
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
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']
				min_dist = sys.maxsize

				closest_market = min(markets, key = lambda market: 
					get_dist(float(latitude), float(longitude), float(market.latitude), float(market.longitude))
									)

				closest_market = json.dumps({'id': closest_market.market_id,
											'name': closest_market.market_name,
											'region': closest_market.region,
											'state': closest_market.state})

				return HttpResponse(closest_market, content_type = 'application/json')
			else:
				return HttpResponse("arguments aren't defined")
		else:
			return HttpResponse("latitude and longitude arguments necessary in request")

	else:
		return HttpResponse("Only POST request is accepted")