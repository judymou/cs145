import sqlalchemy

class ConnectionPoolEngine(object):
    engine = None
    def __init__(self):
        if self.engine == None:
            #self.engine = sqlalchemy.create_engine('sqlite:////Users/belovedjudymou/Documents/schoolProject/cs145/mysite/sqlite3db/mydb.db', echo=True)
            self.engine = sqlalchemy.create_engine('mysql://judymou:onomnom@localhost/onomnomdb', echo=True)
    
    def getPool(self):
        return self.engine

#a = ConnectionPoolEngine().getPool()
#conn = a.connect()
#conn.execute("select * from products_item")
#conn.close()