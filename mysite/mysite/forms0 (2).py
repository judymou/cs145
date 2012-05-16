from django import forms

class ProductForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    product_url = forms.URLField()
