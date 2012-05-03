#!/usr/bin/python

from collections import deque # Efficiently implements a queue
from multiprocessing import Process, Value, Array, Queue
from fetcher import fetch_links
from parser import parse_link
import re
import sys

def fetch_urls(urlQueue, urlQueueMaySeen, limit, processed):
    ''' This function takes in a queue of URLs to fetch and the number of URLs
    to fetch and returns a dictionary representing a histogram of linkcount vs
    frequency.

    When you are make this concurrent think about 3 things:
     - What are the inputs (unique, unseen URLs)
     - What are the outputs (outbound link count, URLs on page)
     - When should the function continue? (processed < limit)
    Think about how to communicate all of this data.  It may be useful
    to use the main() function as a sort of master process.
    '''
    # Restrict URLs to Caltech domain with this regex
    matchRE = re.compile("^https?://([a-z0-9]+\.)*(amazon|express|forever21|bestbuy)\.com/?")

    while processed.value < limit.value:

        url = urlQueue.get() #get the current url
        print "Parsing " + url
        parse_link(url)
        print "Fetching " + str(processed.value + 1) + "/" + str(limit.value) + ": " + url
        links = fetch_links(url) #fetch more link from current url

        if not links: #fetch again if no links from current url
            print "nope"
            continue
        
        processed.value += 1 #update processed value
        
        # Filter out URLs which aren't in the caltech domain
        links = filter(matchRE.match, links)
        
        for link in links: #add all the links to the queue (it will check if it got seen before later)
            urlQueueMaySeen.put(link)

if __name__ == "__main__":
    try: 
        limit = Value('i', 200) #max limit of process it can run
        processed = Value('i', 0) # Number of URLs processed
        urlQueue = Queue() #all unprocessed url
        urlQueueMaySeen = Queue() #all url(might or might not seen)
        
        amazon = "http://www.amazon.com/Hamilton-Beach-51101B-Personal-Blender/dp/B0017XHSAE/ref=sr_1_1?ie=UTF8&qid=1335956312&sr=8-1"
        express = "http://www.express.com/ikat-print-double-v-wedge-tee-45922-682/control/show/3/index.pro"
        forever21 = "http://www.forever21.com/Product/Product.aspx?BR=f21&Category=top&ProductID=2000038004&VariantID="
        bestbuy = "http://www.bestbuy.com/site/Garmin+-+n%26%23252%3Bvi+2455LMT+GPS/3054065.p?id=1218374933088&skuId=3054065&st=Garmin_GPS_offer_20120429&cp=1&lp=1"
        seen = {}
        seen[amazon] = True
        seen[express] = True
        seen[forever21] = True
        seen[bestbuy] = True
        urlQueue.put(amazon)  
        urlQueue.put(express)
        urlQueue.put(forever21)
        urlQueue.put(bestbuy)
        
        listProcess = []
        for i in range(6): #add five processes
            listProcess.append(Process(target= fetch_urls, args = (urlQueue, urlQueueMaySeen, limit, processed)))
    
        for p in listProcess: #start the processes
            p.start()
    
        while processed.value < limit.value:
            link = urlQueueMaySeen.get()
            if link not in seen: # Filter out URLs we've seen before
                seen[link] = True
                urlQueue.put(link) #put into the list to be explored
    
        for p in listProcess: #end the processes
            p.join()
        
        for p in listProcess:
            p.terminate()
        
        print "here"
    except:
        pass
