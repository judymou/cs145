'''Script to be run by cronjob. Goes through each item in database and updates
price'''
from time import gmtime, strftime
from webscraper import *
from databaseUtil import DatabaseUtil

if __name__ == "__main__":
    pathname = "/home/tma/host2/Users/tma/cs145new/mysite/mysite/script_log.txt"
    dbpath = "/home/tma/host2/Users/tma/cs145new/mysite/sqlite3db/mydb.db"
    localtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    try:
        log = open(pathname, "a")
        myDB = DatabaseUtil(dbpath)
        
        # Go through every url in database and check for any changes
        urls = myDB.selectAllURLs()
        for url in urls:
            productName, productId, productPrice, storeName = parseUrl(url[0])
            myDB.update(productId, storeName, productPrice[1:])
    except IOError:
        print "Error: Missing log file...creating new log file"
        log = open(pathname, "w")
    except Exception, e:
        log.write("ERROR at "+ localtime + "\n")
        log.write(str(e) + "\n")
    else:
        log.write("Successful cronjob at " + localtime + "\n")
    finally:
        log.close()

