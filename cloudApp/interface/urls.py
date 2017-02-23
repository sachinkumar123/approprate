from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^market/$', views.market_home),
    url(r'^item/$', views.item_home),
    url(r'^local_market/$', views.local_market_home),
]
   
