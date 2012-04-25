from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.EmailField(max_length=10)

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

class TempTrackList(models.Model):
    username = models.CharField(max_length=10)
    email = models.EmailField()
    product_url = models.URLField()
