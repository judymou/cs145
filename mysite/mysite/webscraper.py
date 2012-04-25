# PARSE VARIOUS SITES

import urllib
import urllib2
from urlparse import urlparse
import string
import sys
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer
from time import time

'''Parse item details from amazon.com'''
def amazon(html):
    parseDetails = SoupStrainer(attrs={"class":re.compile("(parseasinTitle.*|priceLarge.*)")})
    parseId = SoupStrainer(attrs={"name":re.compile("ASIN.*")})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupId = BeautifulSoup(html, parseId)

    detailsTag = filter(lambda a: a != "\n", soupDetails.findAll(text=True))
    idTag = soupId.findAll(limit=1)

    productName = detailsTag[-2].strip()
    productId = idTag[0]["value"].strip()
    productPrice = detailsTag[-1].strip()

    return productName, productId, productPrice, "amazon"
    
'''Parse item details from bestbuy.com'''
### DOESN'T WORK WITH BESTBUY DEALS :(
def bestbuy(html):
    parseDetails = SoupStrainer("div", {"id":"productsummary"})
    parsePrice = SoupStrainer("span", {"class":"price"})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupPrice = BeautifulSoup(html, parsePrice)

    nameTag = soupDetails.h1.findAll(text=True)
    idTag = soupDetails.findAll(text=re.compile("[0-9]{7}"))
    priceTag = soupPrice.findAll(text=True)

    productName = nameTag[0].strip()
    productId = idTag[0].strip()
    productPrice = priceTag[0].strip()

    return productName, productId, productPrice, "bestbuy"

'''Parse item details from express.com'''
def express(html):
    parseDetails = SoupStrainer("div", {"id":"cat-pro-con-detail"})
    soupDetails = BeautifulSoup(html, parseDetails)
       
    detailsTag = filter(lambda a: a != "\n", soupDetails.findAll(text=True))
    priceTag = soupDetails.findAll(attrs={"class":"cat-pro-price"})

    productName = detailsTag[0].strip()
    productId = detailsTag[1].strip()
    productPrice = priceTag[0].findAll(text=True)[-1].strip()

    return productName, productId, productPrice, "express"

'''Parse item details from forever21.com'''
def forever21(html):
    parseDetails = SoupStrainer(attrs={"id":["ItemName", "product_overview"]})
    parsePrice = SoupStrainer("font",{"style":re.compile("font-family:Verdana, Arial, Helvetica, sans-serif.*")})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupPrice = BeautifulSoup(html, parsePrice)

    detailsTag = soupDetails.findAll(text=True)
    priceTag = soupPrice.findAll(text=True)

    productName = detailsTag[0].strip()
    productId = detailsTag[-1].strip()[-10:]
    productPrice = re.search("\$.*", priceTag[-1].strip()).group()
    
    return productName, productId, productPrice, "forever21"

'''Parse item details from walmart.com'''
### NEED TO ADD CAPABILITIES FOR SUBDOMAINS SUCH AS photos.walmart.com
def walmart(html):
    parseDetails = SoupStrainer(attrs={"class":["productTitle", "bigPriceText1', 'smallPriceText1"]})
    parseId = SoupStrainer(attrs={"name":"product_id"})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupId = BeautifulSoup(html, parseId)

    detailsTag = soupDetails.findAll(text=True)
    idTag = soupId.findAll()

    productName = detailsTag[0].strip()
    productId = idTag[0]["value"].strip()
    productPrice = detailsTag[1].strip() + detailsTag[2].strip()

    return productName, productId, productPrice, "walmart"

'''Parse item details from target.com'''
def target(html):
    parseDetails = SoupStrainer(attrs={"class":["fn","price"]})
    parseId = SoupStrainer(attrs={"name":"product-id"})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupId = BeautifulSoup(html, parseId)

    detailsTag = soupDetails.findAll(text=True)
    idTag = soupId.findAll()

    productName = detailsTag[-1].strip()
    productId = idTag[0]["value"].strip()
    productPrice = detailsTag[0].strip()

    return productName, productId, productPrice, "target"

def parseUrl(givenUrl):
    SUPPORTED_WEBSITES = {"amazon":amazon, "bestbuy":bestbuy, "express":express, 
                          "forever21":forever21, "walmart":walmart,"target":target}
    url = str(givenUrl).lower().strip()

    if url.startswith("http://"):
        page = urllib2.urlopen(url)
    else:
        url = "http://" + url
        page = urllib2.urlopen(url)

    html = page.read()
    page.close()

    hostname = urlparse(url).hostname.split(".")[-2]

    # Call correct function based on hostname
    if SUPPORTED_WEBSITES.has_key(hostname):
        return SUPPORTED_WEBSITES[hostname](html)
    else:
        raise NameError("Sorry we do not support that website")

'''if __name__ == "__main__":
    start = time()
    SUPPORTED_WEBSITES = {"amazon":amazon, "bestbuy":bestbuy, "express":express, 
                          "forever21":forever21, "walmart":walmart,"target":target}

    # Ask user for product url
    url = str(raw_input("Enter a product url: ")).lower().strip()

    try:
        if url.startswith("http://"):
            page = urllib2.urlopen(url)
        else:
            url = "http://" + url
            page = urllib2.urlopen(url)
    except urllib2.URLError:
        print "Please enter a valid url"
        sys.exit(1)

    html = page.read()
    page.close()

    hostname = urlparse(url).hostname.split(".")[-2]

    # Call correct function based on hostname
    if SUPPORTED_WEBSITES.has_key(hostname):
        #SUPPORTED_WEBSITES[hostname](html)
        productName, productId, productPrice = SUPPORTED_WEBSITES[hostname](html)
    else:
        print "Sorry, we do not support that site"
        sys.exit(1)

    elapsed = (time() - start)
        
    print "Product Name: %s" % productName
    print "Product Id: %s" % productId
    print "Prodcut Price: %s" % productPrice
    print "Elapsed Time: %s" % elapsed'''
