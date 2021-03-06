from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.util import ErrorList
from datetime import datetime
from products.models import *
from mysite.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decimal import *
from tagging.models import Tag, TaggedItem
from datetime import date
import random

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})
	
@login_required
def mypage(request):
    # Default form
    form = ItemForm(initial={'item_url':'Enter the url here'})

    # If user enters a url, attempt to track item
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
                                            img_url=item['img_url'],
                                            price_date=item['price_date'])

                # Add tags
                entry.set_tags(item['product_name'].lower())

                # query the item id
                currentItem = Item.objects.filter(product_id=item['product_id'],
                                                  store=item['store_name'])
                currentItemId = currentItem.values()[0]['id']
                print "insert the new price to price history table"
                PriceHistory.objects.create(item_id = currentItemId, 
                                            price = item['product_price']
                                            )
                
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
            return HttpResponseRedirect('/mypage/') 

    # Build table containing all watched items
    userItems = TrackList.objects.filter(user_id=request.user.id)

    query_results = []
    for result in userItems:
        # Convert price to string to be displayed in my_page.html
        price = "$%.02f" % result.item.price
        query_results.append([result.item, price])

    return render_to_response('my_page.html', {'form': form, 'query_results': query_results}, context_instance=RequestContext(request)) 

@login_required
def display_tags(request, myTag):
    # Build table containing all items with same tag
    tag = Tag.objects.filter(name=myTag)
    tagId = tag[0].id
    taggedItems = TaggedItem.objects.filter(tag=tagId)

    query_results = []
    for result in taggedItems:
        # Convert price to string to be displayed in my_page.html
        item_id = result.object_id
        item = Item.objects.filter(id=item_id)
        price = "$%.02f" % item[0].price
        query_results.append([item[0], price])

    return render_to_response('tag.html', {'query_results': query_results}, context_instance=RequestContext(request))

@login_required
def my_product(request, itemId):
    # Default form
    form = PriceForm(initial={'price':'Enter new notification price'})
    form2 = EndDateForm()#initial={'end_date':'Enter when to stop tracking'})

    # If user enters a notification price, update TrackList
    # If user enters end date, update TrackList as well
    if request.method == 'POST':
        if "price_box" in request.POST:
            form = PriceForm(request.POST)
            if form.is_valid():
                item = form.cleaned_data
                desired_price = item['price']
                tracked = TrackList.objects.get(user_id=request.user.id,
                                                item_id=itemId)
                tracked.desired_price = desired_price
                tracked.save()
                return HttpResponseRedirect('/product/'+str(itemId))
        else:
            form = EndDateForm(request.POST)
            if form.is_valid():
                item = form.cleaned_data
                end_date = item['end_date']
                tracked = TrackList.objects.get(user_id=request.user.id,
                                                item_id=itemId)
                tracked.end_date = end_date
                tracked.save()
                return HttpResponseRedirect('/product/'+str(itemId))

    # Otherwise, build table containing all items with same tag
    mainItem = Item.objects.get(id=itemId)
    price = "$%.02f" % mainItem.price
    
    # Create recommendation list
    item_tags = TaggedItem.objects.filter(object_id = itemId)
    query_results = []
    for t in item_tags:
        query_results +=(TaggedItem.objects.filter(tag_id = t.tag_id).values_list("object_id", flat=True))
    
    # Remove already tracked items
    recommend_list = []    
    item_ids = list(set(query_results))
    item_ids.remove(int(itemId))

    already_tracked = TrackList.objects.filter(user_id=request.user.id)
    for already in already_tracked:
        # When item is current item, get notification price and end date
        if int(already.item_id) == int(itemId):
            print already.item_id
            print already.user_id
            print already.desired_price
            print already.end_date
            if already.desired_price == None:
                desired_price = "No price specified"
            else:
                desired_price = "$%.02f" % already.desired_price
            if already.end_date== None:
                end_date = "No end date specified"
            else:
                end_date = already.end_date
        # Else remove other tracked items
        if int(already.item_id) in item_ids:
            item_ids.remove(int(already.item_id))

    # Just want to show first 7 recommendations and randomize
    random.shuffle(item_ids)
    item_ids = item_ids[:7]
    for i in item_ids:
        item = Item.objects.get(id = i)
        price = "$%.02f" % item.price
        recommend_list.append([item, price])
    
    # Build comparison list
    query_list = list(Item.objects.filter(name=mainItem.name))
    query_list.remove(mainItem)
    same_items = []
    for item in query_list:
        price = "$%.02f" % item.price
        same_items.append([item, price])

    # Build price history
    history_table = []
    temp = PriceHistory.objects.filter(item_id = itemId)
    for t in temp:
        price = "$%.02f" % t.price
        date = t.price_date
        history_table.append([date, price])
    
    return render_to_response('my_product.html', {'form': form, 'form2': form2, 'mainItem': mainItem, 'price': price, 'recommend_list': recommend_list, 'same_list': same_items, 'desired_price': desired_price, 'end_date': end_date, 'history_table' : history_table}, context_instance=RequestContext(request))

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

@login_required
def track_item(request, itemId):
    items = TrackList.objects.filter(user_id = request.user.id, item_id = itemId)
    if (items.count() == 0):
        TrackList.objects.create(user_id = request.user.id, item_id = itemId)
    return HttpResponseRedirect('/mypage/') 

@login_required
def untrack_item(request, itemId):
    items = TrackList.objects.filter(user_id = request.user.id, item_id = itemId)
    for i in items:
        i.delete()
    return HttpResponseRedirect('/mypage/') 



