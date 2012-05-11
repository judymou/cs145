from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import datetime
from products.models import TempTrackList
from mysite.forms import ProductForm
from django.core.mail import send_mail

def hello(request):
    return HttpResponse("Hello world")

@csrf_exempt	
def product(request):
    error = False
    if request.method == 'POST':
       form = ProductForm(request.POST)
       if form.is_valid():
           item = form.cleaned_data
           t1 = TempTrackList.objects.create(username=item['username'],email = item['email'], product_url = item['product_url'])
           return render_to_response('current_datetime.html', {'error': error})
    else:
       form = ProductForm(initial= {'username': 'ILoveShopping', 'email':'judy@yahoo.com', 'product_url':'http://haha'})
    return render_to_response('welcome.html', {'form': form })

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})



