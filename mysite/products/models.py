from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    product_id = models.CharField(max_length=20)
    store = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits = 10, decimal_places=2)
    url = models.URLField()
    price_date = models.DateField()

class TrackList(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    
class PriceHistory(models.Model):
    item = models.ForeignKey(Item)
    price = models.DecimalField(max_digits = 10, decimal_places=2)
    price_date = models.DateField()

