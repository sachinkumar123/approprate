from __future__ import unicode_literals

from django.db import models
from .indian_states import STATE_CHOICES

class Market(models.Model):
    """
    Market details, it consists of just Indian states
    """
    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return '%s' % (self.market_name)

    market_id = models.AutoField(primary_key=True)
    market_name = models.TextField(max_length=80, unique=True)
    region = models.TextField(max_length=60)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

class Item(models.Model):
    """
    Item details, it can be fruit or vegetable
    """
    def __str__(self):
    	return '%s' % (self.item_name)

    item_name = models.CharField(max_length=30, unique=True)
    item_id = models.AutoField(primary_key=True)
    #item_image_url = models.URLField(default='http://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/articles/health_tools/12_powerhouse_vegetables_slideshow/intro_cream_of_crop.jpg')


class LocalMarketData(models.Model):
    """
    Contains price for every item available in a given market.
    """
    class Meta:
        unique_together = ('item_id', 'market_id')

    def __str__(self):
       return '%s at %s' % (self.item_id, self.market_id)

    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
