from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from products.models import *
from mysite.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})
	
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

def login(request):
    error = False
    if request.method == 'POST':
        print "hi"
        form = LoginForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            # save user information in products_user table
            t1 = User.objects.create(username=item['username'], email=item['email'], password=item['password'])
            #return render_to_response('current_datetime.html', {'error': error})
            return HttpResponseRedirect('/mypage/')
    else:
        form = LoginForm(initial= {'email':'judy@yahoo.com', 'password':'abc123'})
    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
    
def lost(request):
    if request.method == 'POST':
        form = Lost(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            t1 = TempTrackList.objects.create(email = item['email'])
            return render_to_response('current_datetime.html', {'error': error})
    else:
        form = LoginForm(initial= {'email':'why_why@yahoo.com'})
    return render_to_response('lost.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def mypage(request):
    print request.user.id
    return render_to_response('my_page.html')


