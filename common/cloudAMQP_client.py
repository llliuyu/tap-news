''' setup cloudAMQP client '''  # pylint: disable=invalid-name
import json
import pika


class CloudAMQPClient(object):
    '''  setup cloudAMQP client '''

    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def sendMessage(self, message):
        ''' send message to a queue '''
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print '[x] sent message to %s: %s' % (self.queue_name, message)
        queue = self.channel.queue_declare(self.queue_name)
        print 'message numbers:' + str(queue.method.message_count)

    def getMessage(self):
        ''' receive a message from queue '''
        method_frame, header_frame, body = self.channel.basic_get(  # pylint: disable=unused-variable
            self.queue_name)
        if method_frame:
            print '[x] received message from %s: %s' % (self.queue_name, body)
            queue = self.channel.queue_declare(self.queue_name)
            print 'message numbers:' + str(queue.method.message_count)
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
    
    def getMessage_count(self):
        queue = self.channel.queue_declare(self.queue_name)
        return queue.method.message_count
            
    def sleep(self, seconds):
        ''' BlockingConnection.sleep is a safer way to sleep than time.sleep().'''
        self.connection.sleep(seconds)
