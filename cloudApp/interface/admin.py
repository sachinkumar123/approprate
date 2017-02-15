from django.contrib import admin
from .models import Market, LocalMarketData, Item

# Register your models here.
admin.site.register(Market)
admin.site.register(LocalMarketData)
admin.site.register(Item)