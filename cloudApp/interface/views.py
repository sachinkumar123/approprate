from django.http import HttpResponse , StreamingHttpResponse
from django.shortcuts import render
from django.core import serializers
import time, math
from .models import Market, Item, LocalMarketData
from decimal import Decimal
import logging

# to CSRF exempt 
from django.views.decorators.csrf import csrf_exempt

try:
    from django.utils import simplejson as json
except ImportError:
	import json

def home(request):
	return HttpResponse("<h1>Home</h1>")

def get_dist(x1,y1,x2,y2):	
	return pow((pow(x1-x2,2)+pow(y1-y2,2)), 0.5)

@csrf_exempt
def market_home(request):

	if request.POST:
		if 'latitude' in request.POST.keys() and 'longitude' in request.POST.keys():
			if request.POST['latitude'] and request.POST['longitude']:
				markets = list(Market.objects.all())
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']
				min=10000000

				logger = logging.getLogger(__name__)
				logging.basicConfig()
				logger.setLevel(logging.INFO)
				logger.info(Market.objects.all())


				for market in markets:
					dist = get_dist(float(latitude), float(longitude), float(market.latitude), float(market.longitude))
					if dist < min:
						min = dist
						closest_market = market	

				#print(closest_market)

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

def item_home(request):

	'''
	if request.POST :
		if 'item_name' in request.POST.keys() :
			if request.POST['item_name']:
				items=Item.objects.all
				it_name=request.POST['item_name']
				if
				it_id=request.POST['']
				if x in item_name:
					it_id=item_id
				context={
					"queryset":queryset,
					"item_id":it_id,
				}
		if 'item_id' in request.POST.keys():
			if request.POST['item_id']:
				items	
	'''

	


def local_market_home(request):
	queryset=LocalMarketData.objects.all
'''return render(request,"",context)
'''
# Create your views here.
 