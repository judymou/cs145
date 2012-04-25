from django import forms

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