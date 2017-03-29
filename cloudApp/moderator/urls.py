from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add_market/$', views.add_market),
    url(r'^add_item/$', views.add_item),
    url(r'^update_item/$', views.update_item),
    url(r'^update_market/$', views.update_market),
]