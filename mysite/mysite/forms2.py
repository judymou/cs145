from django import forms

class ProductForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    product_url = forms.URLField()

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.EmailField()
    
class Lost(forms.Form):
    email = forms.CharField()