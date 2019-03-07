'''
Created on Jun 13, 2017

@author: daniel
'''
from tornado.web import RequestHandler

class HttpHandler(RequestHandler):

    def initialize(self, external_ip):
        self.external_ip = external_ip

    def post(self, file_name=None):
        print("Page {} fetched via post".format(file_name))

        if file_name:
            self.get(file_name)

    def get(self, file_name):
        print("Page {} fetched via get".format(file_name))

        self.render(file_name,
                    server_ip=self.external_ip)


class HttpHandlerIndex(HttpHandler):

    def get(self):
        super(HttpHandlerIndex, self).get("index.html")
