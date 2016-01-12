#!/usr/bin/python
import os
import sys
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.autoreload

from datetime import timedelta
from multiprocessing import Process, Queue
import time
sys.path.append( 'src' )
sys.path.append( 'src/client/webserver' )
sys.path.append( 'src/core' )
sys.path.append( 'src/usercode' )
from handlers import *
from core import *
from main import *

class Server :

    clients = []

    def __init__( self, serverqueue, clientqueue ) :
        self.game = get_game()
        Game.set_game( self.game )
        self.serverqueue = serverqueue
        self.clientqueue = clientqueue
        while True :
            messages = self.get_messages()
            self.game.update( messages )
            self.send_messages()
            time.sleep(0.05)

    def get_messages( self ) :
        messages = []
        while not self.serverqueue.empty() :
            raw_message = self.serverqueue.get()
            try:
                json_message = json.loads( raw_message[1] )
                messages += [(raw_message[0],json_message)]
            except Exception as e:
                if raw_message[1] == 'NEW' :
                    self.add_client(raw_message[0])
                    continue
                print raw_message[1], 'is not json HEY'
        return messages

    def send_messages( self ) :
        for client in self.game.clients :
            new_data = client.fetch_data()
            if bool(new_data) == True :
                print new_data
                self.clientqueue.put( (str(client.id), new_data ) )

    def add_client( self, id ) :
        self.clients += [id]
        self.game.add_client( id )

def server( serverqueue, clientqueue ) :
    Server( serverqueue, clientqueue )

class Client(tornado.websocket.WebSocketHandler):

    clients = []
    all_messages = {}

    def initialize(self, clientqueue):
        self.clientqueue = clientqueue
        self.closed = False

    def open(self):
        self.clients += [self]
        serverqueue.put((self.clients.index(self),'NEW'))
        self.schedule_update()
        print("New client")

    def schedule_update(self):
        if not self.closed :
            self.timeout = tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=0.05), self.update_client)

    def update_client(self):
        if not self.closed :
            data = all_messages.get( str(self.clients.index(self) ) )
            if data != [] and data != None :
                message = {'d':data}
                all_messages[ str(self.clients.index(self)) ] = []
                self.write_message(message)
        self.schedule_update()

    def on_message(self, message):
        serverqueue.put((self.clients.index(self),message))

    def on_close(self):
        self.closed = True
        print("WebSocket closed")

def make_app(clientqueue):
    public_root = os.path.join(os.path.dirname(__file__), 'src/client/public')
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", Client, dict(clientqueue=clientqueue)),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': public_root}),
    ])

def get_messages():
    messages = []
    while not clientqueue.empty() :
        messages += [clientqueue.get()]
    for message in messages :
        id = message[0]
        data = message[1]
        if all_messages.get(id) == None :
            all_messages[id] = []
        all_messages[id] += [data]
    tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=0.05), get_messages)

if __name__ == "__main__":
    all_messages = {}
    clientqueue = Queue()
    app = make_app( clientqueue )
    app.listen(8888)
    serverqueue = Queue()
    serverprocess = Process(target=server, args=(serverqueue,clientqueue,))
    serverprocess.start()
    tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=0.05), get_messages)
    for dir, _, files in os.walk('src/client'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
    tornado.ioloop.IOLoop.current().start()
