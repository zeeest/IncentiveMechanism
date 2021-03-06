from SuperNode.couchdatabase import store
import coefficients as k
import logging


loggerReg = logging.getLogger('Register')

def Register(ON_IP,ON_PORT,capacity,resource):
    global  loggerReg

    print "ON_IP",ON_IP, \
        "ON_PORT", ON_PORT, \
        "capacity", capacity, \
        "resource", resource

    json_doc = {
                "_id" : ON_IP,
                "info" : {
                    "capacity": capacity, \
                    "resource" : resource, \
                    "avail" : resource, \
                    "credit" : resource, \
                    "effort" : float(resource * k.res)/(capacity * k.cap) \
                 },
                "providedTo" : {},  ## { 'nodeID' : 'amount' }
                "suppliedFrom" : {}  ## {'nodeID' : [ {'amount' : amount ,'timestamp' : timestamp}, .. ]
        }


    store.call_db().store_document(json_doc)

    ## TODO : record sliver info ##
    loggerReg.info("The node:%s is registered with capacity:%s resources:%s" %(ON_IP,capacity,resource))
    return "REGISTERED"