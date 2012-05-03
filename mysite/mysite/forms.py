from django import forms
from mysite.webscraper import *
from datetime import date
from products.models import *

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

class ItemForm(forms.Form):
    item_url = forms.URLField()

    def clean(self):
        cleaned_data = super(ItemForm, self).clean()
        item_url = cleaned_data.get("item_url")

        try:
            # If url is valid, add relevant info to cleaned_data
            productName, productId, productPrice, storeName = parseUrl(item_url)
            # conver the price to a double
            productPrice = round(float(productPrice), 3)
            
            cleaned_data["product_name"] = productName
            cleaned_data["product_id"] = productId
            cleaned_data["product_price"] = productPrice
            cleaned_data["store_name"] = storeName
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
