import datetime
import logging
import operations
import pyjsonrpc
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 4040


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    ''' Test method '''
    @pyjsonrpc.rpcmethod
    def add(self, num1, num2):  # pylint: disable=no-self-use
        ''' add two numbers '''
        print "add is called with %d and %d" % (num1, num2)
        return num1 + num2
    
    ''' Get news summaries for a user '''
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num, user_ip):
        starttime = datetime.datetime.now()
        response = operations.getNewsSummariesForUser(user_id, page_num, user_ip)
        endtime = datetime.datetime.now()
        diff = int((endtime - starttime).microseconds/1000)

        logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s',
                datefmt='%a %d %b %Y %H:%M:%S' + ',',
                filename='../logging/user_requests_' + time.strftime('%m-%d-%Y', time.localtime()) +'.log',
                filemode='a')
        logging.info(
                    'operations.getNewsSummariesForUser' + ', ' +
                    str(diff) + ' ms, ' +
                    'event_name : ' + 'news_list_request' + ', ' + 
                    'user_id : ' + str(user_id) + ', ' +
                    'user_ip : ' + str(user_ip))

        return response

    ''' Get preference for a user '''
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):

        response = operations.getPreferenceForUser(user_id)
        return response

    
    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id, user_ip):
        return operations.logNewsClickForUser(user_id, news_id, user_ip)


# Threading HTTP Server
HTTPSERVER = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print 'starting http server on %s:%d' % (SERVER_HOST, SERVER_PORT)
HTTPSERVER.serve_forever()
