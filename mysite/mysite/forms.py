from django import forms
from django.forms.extras.widgets import SelectDateWidget
from mysite.webscraper import *
from datetime import date
from products.models import *
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=10)
    
class ProductForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    product_url = forms.URLField()

class Lost(forms.Form):
    email = forms.EmailField()

class PriceForm(forms.Form):
    price = forms.DecimalField()
    
class EndDateForm(forms.Form):
    end_date = forms.DateField(widget=SelectDateWidget())

class ItemForm(forms.Form):
    item_url = forms.URLField()

    def clean(self):
        cleaned_data = super(ItemForm, self).clean()
        item_url = cleaned_data.get("item_url")

        try:
            # If url is valid, add relevant info to cleaned_data
            itemDetails = parseUrl(item_url)
            # convert the price to a double
            productPrice = float(itemDetails[2])
            
            cleaned_data["product_name"] = itemDetails[0]
            cleaned_data["product_id"] = itemDetails[1]
            cleaned_data["product_price"] = str(productPrice)
            cleaned_data["img_url"] = itemDetails[3]
            cleaned_data["store_name"] = itemDetails[4]
            cleaned_data["price_date"] = date.today()

        except urllib2.URLError:
            raise forms.ValidationError("Please enter a valid url")
        except NameError, e:
            raise forms.ValidationError(e)
        except Exception, e:
            raise forms.ValidationError("Sorry, we couldn't find your item")

        #if Item.objects.filter(product_id = productId, store = storeName): 
        #    raise forms.ValidationError("You are already watching this item!")
       
        return cleaned_data
