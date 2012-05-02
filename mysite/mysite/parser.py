from webscraper import *
from ConnectionPoolEngine import ConnectionPoolEngine

def parse_link(url):
    try:
        conn = ConnectionPoolEngine().getPool().connect()
        productName, productId, productPrice, storeName = parseUrl(url)
        query = 'select id, price from products_item where product_id = \'' + str(productId) + "\' and store = \'" + str(storeName) + "\'"
        result = conn.execute(query)
        row = result.fetchone()
        if (row == None):
            myValues = (productId, storeName, productName, productPrice, url);
            conn.execute('insert into products_item (product_id, store, name, price, url) values (?, ?, ?, ?, ?)', myValues)
        elif(productPrice < row['price']):
            conn.execute('update products_item set price =' + str(productPrice) + ', price_date = current_timestamp where id = ' + str(row['id']))
            myValues = (row['id'], productPrice)
            conn.execute('insert into price_history (item_id, price) values (?,?)', myValues)
        result.close()
        conn.close()
    except Exception, e:
        print str(e)

if __name__ == "__main__":
    parse_link("http://www.express.com/classic-fit-belted-striped-shorts-46091-927/refine/size/36/control/page/2/show/3/index.pro")