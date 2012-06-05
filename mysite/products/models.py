from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from datetime import datetime

# Create your models here.
class Item(models.Model):
    product_id = models.CharField(max_length=20)
    store = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits = 10, decimal_places=2)
    url = models.URLField()
    img_url = models.URLField()
    price_date = models.DateField()
    tags = TagField()

    def get_tags(self):
        return Tag.objects.get_for_object(self) 

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

class TrackList(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    desired_price = models.DecimalField(max_digits = 20, decimal_places=2)
    end_date = models.DateField()
    
class PriceHistory(models.Model):
    item = models.ForeignKey(Item)
    price = models.DecimalField(max_digits = 10, decimal_places=2)
    price_date=models.DateTimeField(default=datetime.now)

