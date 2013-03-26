import SimpleXMLRPCServer
from SuperNode.query_handler import register as res
from SuperNode.query_handler import request as req
from SuperNode.query_handler import heartbeat as h
from SuperNode.query_handler import nondefined as non

ON_IP=None
ON_PORT=None

class LoggingSimpleXMLRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Overides the default SimpleXMLRPCRequestHander to support logging.  Logs
    client IP and the XML request and response.
    """

    def do_POST(self):
        global ON_IP, ON_PORT
        ON_IP, ON_PORT = self.client_address
	# Log client IP and Port
        # logger.info('Client IP: %s - Port: %s' % (clientIP, port))
        print 'Client IP:', ON_IP, '- Port:', ON_PORT
	try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # Log client request
	    #logger.info('Client request: \n%s\n' % data)

            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
	    # Log server response
            # logger.info('Server response: \n%s\n' % response)

	except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

class Queries:
        global ON_IP, ON_PORT
        def register(self, capacity, resource):
            return res.Register(ON_IP,ON_PORT,capacity,resource)
            #return x+y+100

        def request(self, reqAmount, reqDuration):
                return req.Request(ON_IP,ON_PORT,reqAmount, reqDuration)

        def heartbeat(self):
                return h.heartbeat.Heartbeat(ON_IP,ON_PORT)

        def nondefined(self, x, y):
                return non.nondefined()
