#!/usr/bin/python

from collections import deque # Efficiently implements a queue
from multiprocessing import Process, Value, Array, Queue
from fetcher import fetch_links
from parser import parse_link
import re
import sys
#it might be an error after all my program has terminated: I search up online, it might be a error from python
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
    matchRE = re.compile("^https?://([a-z0-9]+\.)*express\.com/?")

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
        limit = Value('i', 10) #max limit of process it can run
        processed = Value('i', 0) # Number of URLs processed
        urlQueue = Queue() #all unprocessed url
        urlQueueMaySeen = Queue() #all url(might or might not seen)
        
        seen = {"http://www.express.com/classic-fit-belted-striped-shorts-46091-927/refine/size/36/control/page/2/show/3/index.pro" : True} # Set of URLs we've seen before
        urlQueue.put("http://www.express.com/classic-fit-belted-striped-shorts-46091-927/refine/size/36/control/page/2/show/3/index.pro")  
        
        listProcess = []
        for i in range(5): #add five processes
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
