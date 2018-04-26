#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import tornado.ioloop
import sockjs.tornado
import logging
from datetime import datetime
# Logging
logging.basicConfig(level=logging.INFO, filename='chat_server.log', format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
log = logging.getLogger('chat_server')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)


class ChatConnection(sockjs.tornado.SockJSConnection):
    participants = set()

    def on_open(self, info):
        msg = "user joined."
        log.info(msg)
        self.broadcast(self.participants, '{} - {}'.format(self.stamp(), msg))
        self.participants.add(self)

    def on_message(self, message):
        log.info(message)
        self.broadcast(self.participants, '{} - {}'.format(self.stamp(), message))

    def on_close(self):
        msg = "user left."
        log.info(msg)
        self.participants.remove(self)
        self.broadcast(self.participants, '{} - {}'.format(self.stamp(), msg))

    @staticmethod
    def stamp():
        now = datetime.now()
        return now.strftime('%x %X')


if __name__ == "__main__":
    # Check if we need to use custom port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8180
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')
    app = tornado.web.Application(ChatRouter.urls)
    app.listen(port)
    log.info("Server started at port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()
