from django.contrib import admin
from .models import Market, LocalMarketData, Item

# Register your models here.
class MarketModelAdmin(admin.ModelAdmin):
	list_display=["market_id","market_name","state","latitude","longitude"]
	list_display_links=["market_id"]
	list_editable=["market_name"]
	list_filter=["state","market_name","region"]
	search_fields=["state","region"]

	class Meta:
		model=Market

class ItemModelAdmin(admin.ModelAdmin):
	
	list_display=["item_name","item_id"]
	list_display_links=["item_id"]
	list_editable=["item_name"]
	list_filter=["item_name","item_id"]
	search_fields=["item_name"]
	class Meta:
		model=Item

class LocalMarketModelAdmin(admin.ModelAdmin):
	list_display=["price","market_id","item_id"]
	list_display_links=["market_id"]
	list_editable=["price"]
	list_filter=["price","market_id","item_id"]
	search_fields=["price","market_id","item_id"]
	class Meta:
		model=LocalMarketData


admin.site.register(Market,MarketModelAdmin) 
admin.site.register(LocalMarketData,LocalMarketModelAdmin)
admin.site.register(Item,ItemModelAdmin)