from webscraper import *
from databaseUtil import DatabaseUtil



def parse_link(url):
    dbpath = "/Users/belovedjudymou/Documents/schoolProject/cs145/mysite/sqlite3db/mydb.db"
    myDB = DatabaseUtil(dbpath)
    try: 
        productName, productId, productPrice, storeName = parseUrl(url)
        print "HELOOOOOOOOOOO"
        myDB.insert(productId, storeName, productName, productPrice, url)
    except Exception, e:
        print str(e)
    