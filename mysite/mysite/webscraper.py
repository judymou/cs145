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
    productPrice = productPrice[1:]

    parseImg = SoupStrainer("img", {"alt":re.compile(productName.split()[0])})
    soupImg = BeautifulSoup(html, parseImg)
    imgTag = soupImg.findAll(limit=1)
    productImg = imgTag[0]["src"].strip()

    return [productName, productId, productPrice, productImg, "amazon"]
    
'''Parse item details from bestbuy.com'''
### DOESN'T WORK WITH BESTBUY DEALS :(
def bestbuy(html):
    parseDetails = SoupStrainer("div", {"id":"productsummary"})
    parsePrice = SoupStrainer("span", {"class":"price"})
    parseImg = SoupStrainer("img", {"src":re.compile("images/products")})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupPrice = BeautifulSoup(html, parsePrice)
    soupImg = BeautifulSoup(html, parseImg)

    nameTag = soupDetails.h1.findAll(text=True)
    idTag = soupDetails.findAll(text=re.compile("[0-9]{7}"))
    priceTag = soupPrice.findAll(text=True)
    imgTag = soupImg.findAll(limit=1)

    productName = nameTag[0].strip()
    productId = idTag[0].strip()
    productPrice = priceTag[0].strip()
    productPrice = productPrice[1:]
    productImg = imgTag[0]["src"].strip()

    return [productName, productId, productPrice, productImg, "bestbuy"]

'''Parse item details from express.com'''
def express(html):
    parseDetails = SoupStrainer("div", {"id":"cat-pro-con-detail"})
    parseImg = SoupStrainer("link", {"href":re.compile("s7d5")})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupImg = BeautifulSoup(html, parseImg)
       
    detailsTag = filter(lambda a: a != "\n", soupDetails.findAll(text=True))
    priceTag = soupDetails.findAll(attrs={"class":"cat-pro-price"})
    imgTag = soupImg.findAll(limit=1)

    productName = detailsTag[0].strip()
    productId = detailsTag[1].strip()
    productPrice = priceTag[0].findAll(text=True)[-1].strip()
    productPrice = productPrice[1:]
    productImg = imgTag[0]["href"].strip()

    return [productName, productId, productPrice, productImg, "express"]

'''Parse item details from forever21.com'''
def forever21(html):
    parseDetails = SoupStrainer(attrs={"id":["ItemName", "product_overview", "ctl00_MainContent_productImage"]})
    parsePrice = SoupStrainer("font",{"style":re.compile("font-family:Verdana, Arial, Helvetica, sans-serif.*")})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupPrice = BeautifulSoup(html, parsePrice)

    detailsTag = soupDetails.findAll(text=True)
    priceTag = soupPrice.findAll(text=True)
    imgTag = soupDetails.findAll(limit=1)

    productName = detailsTag[0].strip()
    productId = detailsTag[-1].strip()[-10:]
    productPrice = re.search("\$.*", priceTag[-1].strip()).group()
    productPrice = productPrice[1:]
    productImg = imgTag[0]["src"].strip()
    
    return [productName, productId, productPrice, productImg, "forever21"]

'''Parse item details from walmart.com'''
### NEED TO ADD CAPABILITIES FOR SUBDOMAINS SUCH AS photos.walmart.com
def walmart(html):
    parseDetails = SoupStrainer(attrs={"class":["productTitle", "bigPriceText1", "smallPriceText1"]})
    parseId = SoupStrainer(attrs={"name":"product_id"})
    soupDetails = BeautifulSoup(html, parseDetails)
    soupId = BeautifulSoup(html, parseId)

    detailsTag = soupDetails.findAll(text=True)
    idTag = soupId.findAll()

    productName = detailsTag[0].strip()
    productId = idTag[0]["value"].strip()
    productPrice = detailsTag[1].strip() + detailsTag[2].strip()
    productPrice = productPrice[1:]

    parseImg = SoupStrainer("img", {"alt":re.compile(productName.split()[0])})
    soupImg = BeautifulSoup(html, parseImg)
    imgTag = soupImg.findAll(limit=1)
    productImg = imgTag[0]["src"].strip()

    return [productName, productId, productPrice, productImg, "walmart"]

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
    productPrice = productPrice[1:]
 
    parseImg = SoupStrainer("img", {"alt":re.compile(productName.split()[0])})
    soupImg = BeautifulSoup(html, parseImg)
    imgTag = soupImg.findAll(limit=1)
    productImg = imgTag[0]["src"].strip()

    return [productName, productId, productPrice, productImg, "target"]

'''Programs that wish to use this webscraper should call this function.
   Takes in an url and returns a list containing the following information:
   product_name, id, price, img_url, store_name'''
def parseUrl(givenUrl):
    SUPPORTED_WEBSITES = {"amazon":amazon, "bestbuy":bestbuy, "express":express, 
                          "forever21":forever21, "walmart":walmart,"target":target}

    # Keep url fonts consistent by forcing lowercase and striping any white spaces
    url = str(givenUrl).lower().strip()

    # Check if url starts with http://
    # Sometimes users forget to include http and urllib2 cannot open without that prefix
    if url.startswith("http://"):
        page = urllib2.urlopen(url)
    else:
        url = "http://" + url
        page = urllib2.urlopen(url)

    html = page.read()
    page.close()

    # Grab the domain name
    hostname = urlparse(url).hostname.split(".")[-2]

    # Call correct function based on hostname
    if SUPPORTED_WEBSITES.has_key(hostname):
        return SUPPORTED_WEBSITES[hostname](html)
    else:
        raise NameError("Sorry we do not support that website")

'''if __name__ == "__main__":
    url = "http://www.amazon.com/Transformers-Season-Limited-Edition-Blu-ray/dp/B006JN87UC/ref=sr_1_3?ie=UTF8&qid=1337121354&sr=8-3"

    values = parseUrl(url)
    print values'''
