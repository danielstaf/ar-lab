'''
Created on Jun 12, 2017

@author: daniel
'''

import zmq
#from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
#ioloop.install()

from tornado.websocket import WebSocketHandler
#from tornado.web import Application
#from tornado.ioloop import IOLoop
#ioloop = IOLoop.instance()

from zmq.utils import jsonapi

class ZMQPubSub(object):

    def __init__(self, callback):
        self.callback = callback

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://127.0.0.1:6666')
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.callback)

    def subscribe(self):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def disconnect(self):
        self.stream.close()
        self.socket.close()

class PushWebSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.pubsub = ZMQPubSub(self.on_backend_data)
        self.pubsub.connect()
        self.pubsub.subscribe()
        print('ws opened')

    def on_message(self, message):
        print(message, "hm")
    
    def on_close(self):
        self.pubsub.disconnect()
        print('ws closed')

    def on_backend_data(self, data):
        self.write_message(data[0])
