from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from interface.models import Market
import json


def home(request):
    return HttpResponse("<h1>Moderator Home</h1>")

@csrf_exempt
def get_region(request):
    """Summary
    
    Args:
        request (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    if request.method == "POST":
        if 'username' in request.POST.keys() and 'password' in request.POST.keys():
            if request.POST['username'] and request.POST['password']:
                username = request.POST['username']
                password = request.POST['password']
                """market_data = list(LocalMarketData.objects.filter(market_id__market_name=name))

                market_items = []

                for item in market_data:
                    market_items.append({
                                            'item': item.item_id.item_name,
                                            'price': item.price,
                                            'item-image': item.item_id.item_image_url
                                        })

                market_items = json.dumps(market_items)
                return HttpResponse(market_items, content_type = 'application/json')"""
                user = authenticate(username=username, password=password)
                if user is not None:
                    #return HttpResponse("Successful authentication")
                    markets = list(Market.objects.filter(moderator=user))
                    print(markets)
                    market_data = []
                    for market in markets:
                        market_data.append({
                                        'name': market.market_name,
                                        'region': market.region
                                     })
                    market_data = json.dumps(market_data)
                    return HttpResponse(market_data, content_type = 'application/json')

                else:
                    return HttpResponse("Invalid Username and Password")
            else:
                return HttpResponse("argument username and password is not defined")
        else:
            return HttpResponse("username and password is necessary argument")
    else:
        return HttpResponse("Only POST request is accepted")

def add_market(request):
    pass

def add_item(request):
    pass

def update_item(request):
    pass

def update_market(request):
    pass

def add_moderator(request):
    pass