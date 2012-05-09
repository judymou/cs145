from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.util import ErrorList
import datetime
from products.models import *
from mysite.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decimal import *

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})
	
@login_required
def mypage(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            currentItemId = -1
            
            # Check if item has already been added to database
            result = Item.objects.filter(product_id = item['product_id'], 
                                         store = item['store_name'])
            if (result.count() == 0):
                # insert product info in products_item table
                print "insert new item to products_item"
                entry = Item.objects.create(product_id=item['product_id'],
                                        store=item['store_name'],
                                        name=item['product_name'],
                                        price=item['product_price'],
                                        url=item['item_url'],
                                        price_date=item['price_date'])

                # query the item id
                currentItem = Item.objects.filter(product_id=item['product_id'],
                                                  store=item['store_name'])
                currentItemId = currentItem.values()[0]['id']
                print "insert the new price to price history table"
                PriceHistory.objects.create(item_id = currentItemId, 
                                            price = item['product_price'])
                
            else :
                oldItemInfo = result.values()[0]
                currentItemId = oldItemInfo['id']
                if (item['product_price'] < oldItemInfo['price']):
                    # if product exists already and price has dropped, update
                    # item table and insert into price history.
                    print "update old item in products_item"
                    Item.objects.filter(id = currentItemId).update(
                        price=item['product_price'], 
                        price_date=item['price_date'])
                    print "insert new entry to price history"
                    PriceHistory.objects.create(item_id = currentItemId, 
                                                price = item['product_price'])
            
            # Add product to tracklist if its not tracked
            tracklist = TrackList.objects.filter(user_id=request.user.id, 
                                                 item_id = currentItemId)
            if (tracklist.count() == 0):
                print "add (user, item) to tracklist"
                TrackList.objects.create(user_id= request.user.id, 
                                         item_id= currentItemId)
            return HttpResponseRedirect('/time/') 
    else:
        form = ItemForm(initial={'item_url':'Enter the url here'})
        userItems = TrackList.objects.filter(user_id=request.user.id)

        query_results = []
        for result in userItems:
            query_results.append(result.item)
    return render_to_response('my_page.html', {'form': form, 'query_results': query_results}, context_instance=RequestContext(request)) 

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
            t1 = User.objects.create(username=item['username'],
                                     email=item['email'],
                                     password=item['password'])
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


