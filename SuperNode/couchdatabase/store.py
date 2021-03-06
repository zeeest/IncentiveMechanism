import couchdb
import settings as set
from SuperNode.query_handler import coefficients as k
import logging


loggerDB = logging.getLogger('Database')

db = None

class Database:
    global loggerDB
    def __init__(self, name = set.DB_NAME):
        couch = couchdb.Server(set.DB_SERVER_IP+':'+set.DB_SERVER_PORT)

        try:
            db = couch.create(name)
            loggerDB.info("Database %s is creating" %name )
        except:
            db = couch[name]

        self.db = db

    def store_document (self, doc):
        self.db.save(doc)

    def update_document(self, doc_id, updatedDoc):
        self.db[doc_id] = updatedDoc

    def delete_document(self, doc_id):
        del self.db[doc_id]

    def get_document(self, doc_id):
        return self.db[doc_id]

    def is_exist (self, doc_id):
        return self.db.__contains__(doc_id)

    def get_avail (self, doc_id):
        return self.db[doc_id]['avail']

    def update_credit(self, doc_id, newCredit) : #type :0 = addtoCredit type:1 = set credit
        if self.is_exist(doc_id):
            if self.db[doc_id]['info'].has_key('credit'):
                tempDoc = self.get_document(doc_id)
                tempDoc['info']['credit'] += newCredit
                tempDoc['info']['effort'] = float(tempDoc['info']['credit'] * k.res) / \
                                        (tempDoc['info']['capacity'] * k.cap )
                if tempDoc['info']['effort'] > 1 : tempDoc['info']['effort'] = 1
            else :
                print "There is no 'credit' key in the client doc"
                print "Client doc should be proper"
        else:
            print "non-exist document"

        self.update_document(doc_id, tempDoc)
    #def updateEffort ..


    def get_db(self):
        return self.db

    def delete_gb(self):
        del self.db

    def print_db(self):
        print "------- DB -----------"
        for doc in self.db:
            print self.db[doc]
        print "\n"


def call_db():
    db = Database()
    return db


if __name__ == "__main__":
    myDB = call_db()
    myDB.store_document({'_id':'111', 'info' : { 'capacity':100, 'resoure':34, 'avail' : 34, 'credit':34, 'effort': float(34)/100},
                                       'providedTo' : {},'suppliedFrom' : {}})#  {'timestamp': 111, 'info':{'111':10}}, {'timestamp': 111, 'info':{'222':5} }}})
    myDB.store_document({'_id':'222', 'info' : { 'capacity':200, 'resoure':134, 'avail' : 134, 'credit':134, 'effort': float(134)/200},
                                       'providedTo' : {},'suppliedFrom' : {}})
    myDB.store_document({'_id':'333', 'info' : { 'capacity':300, 'resoure':14, 'avail' : 14, 'credit':14, 'effort':float(14)/300 },
                                       'providedTo' : {},'suppliedFrom' : {}})

    myDB.print_db()

   # doc = myDB.get_document('333')
   # doc['info']['capacity'] = 1111
   # myDB.update_document('333', doc)
   # myDB.print_db()



