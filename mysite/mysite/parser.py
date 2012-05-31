from django.core.mail import send_mail
from webscraper import *
from ConnectionPoolEngine import ConnectionPoolEngine
from tagging.models import Tag, TaggedItem
from products.models import *
from datetime import date
from django.contrib.auth.models import User

def parse_link(myUrl):
    try:        
        itemDetails = parseUrl(myUrl)
        productName= itemDetails[0]
        productId= itemDetails[1]
        productPrice = str(itemDetails[2])
        my_img_url = itemDetails[3]
        storeName = itemDetails[4]
        productPrice = str(round(float(productPrice), 3))
        
        # Check if item has already been added to database
        result = Item.objects.filter(product_id = productId, 
                                     store = storeName)
        if (result.count() == 0):
            # Create Item object
            print "insert new item to products_item"
            entry = Item.objects.create(product_id=productId,
                                        store=storeName,
                                        name=productName,
                                        price=productPrice,
                                        url=myUrl,
                                        img_url=my_img_url,
                                        price_date=date.today())

            # Add tags
            entry.set_tags(productName.lower())

            # query the item id
            currentItem = Item.objects.get(product_id=productId,
                                           store=storeName)
            currentItemId = currentItem.id
            print "insert the new price to price history table"
            PriceHistory.objects.create(item = currentItem, 
                                        price = productPrice)
        elif float(productPrice) < float(result[0].price):
            # Else update tables if new price is lower than old price
            result[0].price = productPrice
            entry = PriceHistory.objects.create(item=result[0],
                                                price=productPrice)
            # Get set of all users tracking this item
            query = TrackList.objects.filter(item=result[0])

            ### TODO ###
            # Possibly add user email to tracklist to avoid the need to query again
            # Or use the email_user function of User model objects
            recipients = []
            for tracklist in query:
                myUser = tracklist.user
                recipients.append(myUser.email)
            print "Sending email"
            send_mail('Price drop', 'Your item has dropped..buy now!', 'shopomnomnom@gmail.com', recipients)
            print "Finished sending"
                
    except Exception, e:
        print str(e)

if __name__ == "__main__":
    parse_link("http://www.express.com/sequin-embellished-shirttail-tank-43797-504/control/page/192/show/3/index.pro?relatedItem=true&relatedItem=true&relatedItem=true&relatedItem=true&relatedItem=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true")
