import sqlite3

class DatabaseUtil(object):
    def __init__(self, dbFilePath):
        self.conn = sqlite3.connect(dbFilePath)
        self.dbCursor = self.conn.cursor()
    
    # product_id varchar
    # name varchar
    # price double
    # url varchar
    def insert(self, productId, name, price, url):
        # example: myValues = ('bb', 'hellob', 1.23, '12345',)
        myValues = (productId, name, price, url);
        self.dbCursor.execute('insert into products_item (product_id, name, price, url) values (?, ?, ?, ?)', myValues)
        self.conn.commit()
        
    def selectUniqueURLs(self):
        self.dbCursor.execute('select url from products_item')
        URLs = self.dbCursor.fetchall()
        print URLs
        return URLs
