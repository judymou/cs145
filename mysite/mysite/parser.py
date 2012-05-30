from django.core.mail import send_mail
from webscraper import *
from ConnectionPoolEngine import ConnectionPoolEngine

def parse_link(url):
    try:
        conn = ConnectionPoolEngine().getPool().connect()
        
        itemDetails = parseUrl(url)
        productName= itemDetails[0]
        productId= itemDetails[1]
        productPrice = str(itemDetails[2])
        img_url = itemDetails[3]
        storeName = itemDetails[4]
        productPrice = round(float(productPrice), 3)
        
        query = 'select id, price from products_item where product_id = \'' + str(productId) + "\' and store = \'" + str(storeName) + "\'"
        result = conn.execute(query)
        row = result.fetchone()
        if (row == None):
            # If item does not exist yet, insert into products_item database
            # Also insert into products_pricehistory to start tracking price
            conn.execute('insert into products_item (product_id, store, name, price, url, img_url) values ( \'' + str(productId) + '\', \'' + str(storeName) + '\', \'' + str(productName) + '\', ' + str(productPrice) + ', \'' + str(url) + '\', \'' + str(img_url) + '\')')
            ### TODO ###
            # Must be more efficient way of fetching new item id
            result = conn.execute(query)
            row = result.fetchone()
            conn.execute('insert into products_pricehistory (item_id, price) values (' + str(row['id']) + ', ' + str(productPrice) + ')')
        elif productPrice < row['price']:
            # Else update tables if new price is lower than old price
            conn.execute('update products_item set price =' + str(productPrice) + ', price_date = current_timestamp where id = ' + str(row['id']))
            myValues = (row['id'], productPrice)
            conn.execute('insert into products_pricehistory (item_id, price) values (' + str(row['id']) + ', ' + str(productPrice) + ')')
            query = 'select user_id from products_tracklist where item_id = \'' + str(row['id']) + "\'"
            result = conn.execute(query)
            ### TODO ###
            # Possibly add user email to tracklist to avoid the need to query again
            # Or use the email_user function of User model objects
            for res in result:
                query = 'select * from auth_user where id = \'' + str(res['user_id']) + "\'"
                userResult = conn.execute(query)
                user = userResult.fetchone()
                send_mail('Price drop', 'Your item has dropped..buy now!', 'shopomnomnom@gmail.com', [str(user['email'])])
                
        result.close()
        conn.close()
    except Exception, e:
        print str(e)

if __name__ == "__main__":
    parse_link("http://www.express.com/sequin-embellished-shirttail-tank-43797-504/control/page/192/show/3/index.pro?relatedItem=true&relatedItem=true&relatedItem=true&relatedItem=true&relatedItem=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true&showBreadcrumb=true")
