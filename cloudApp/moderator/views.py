from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Moderator Home</h1>")

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