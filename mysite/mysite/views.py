from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
import products.models
from mysite.forms import ProductForm


def hello(request):
    return HttpResponse("Hello world")
	

def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            t1 = TempTrackList.objects.create(username=item['username'],email = item['email'], product_url = item['product_url'])
            return HttpResponseRedirect('/hello/')
    else:
        form = ProductForm(initial= {'username': 'ILoveShopping', 'email':'judy@yahoo.com', 'product_url':'http://haha'})
    error = False
    return render_to_response('welcome.html', {'form': form })

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})



