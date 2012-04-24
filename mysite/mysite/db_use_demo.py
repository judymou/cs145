
import urllib
import urllib2
import string
import sys
from BeautifulSoup import BeautifulSoup, SoupStrainer
from time import time
from decimal import *
from databaseUtil import DatabaseUtil

url = 'http://www.amazon.com/gp/product/0123745144/ref=s9_simh_gw_p14_d0_g14_i2?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=center-2&pf_rd_r=07690KXG6VKFA1C6Q93D&pf_rd_t=101&pf_rd_p=470938631&pf_rd_i=507846'
page=urllib2.urlopen(url)
html=page.read()
page.close()

start = time()
targetPage1 = SoupStrainer(id = ['btAsinTitle', 'ASIN'])
targetPage2 = SoupStrainer(attrs={'class':'priceLarge'})
pool1=BeautifulSoup(html, targetPage1)
pool2=BeautifulSoup(html, targetPage2)

print pool1;
print pool2;

asin = pool1.findAll(id = 'ASIN', limit = 1)
asin = asin[0]['value']
title = pool1.findAll(id = 'btAsinTitle', limit=1)
title = title[0].findAll(text=True)
price = pool2.findAll(limit=1)
price = price[0].findAll(text=True)

print "title: %s" % title[0]
print "price: %s" % price[0]
print "asin: %s"  % asin
elapsed = (time() - start)
print elapsed

filePath = "/Users/belovedjudymou/Documents/schoolProject/cs145/mysite/sqlite3db/mydb.db"
myDB = DatabaseUtil(filePath)
#myDB.insert(asin, 'amazon', title[0], float(price[0].replace("$", "")), url)
myDB.selectUniqueURLs('amazon')
myDB.update(asin, 'amazon', 3)

# arrayStores = ['ama', 'best']
# select * from balh where store = amazon