from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^get_closest_market/$', views.get_closest_market),
    url(r'^get_nearby_markets/$', views.get_nearby_markets),
    url(r'^get_markets_in_region/$', views.get_markets_in_region),
    url(r'^get_regional_markets_having_item/$', views.get_regional_markets_having_item),
]
   
