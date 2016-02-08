#!/usr/bin/env python

import os
import sys
import logging
import threading
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../common'))
from server import *

from socketserver import UDPServer, BaseRequestHandler
from threading import Thread

USAGE = "Usage: main.py <host> <port>"

class UDPDiscoveryHandler(BaseRequestHandler):

    def handle(self):
        if self.request[0].decode("UTF-8") == "I_NEED_A_BATTLESHIP_PLUS_PLUS_SERVER":
            socket = self.request[1]
            socket.sendto("I_AM_A_BATTLESHIP_PLUS_PLUS_SERVER".encode("UTF-8"), self.client_address)

def startUDPDiscovery():
    server = UDPServer(("", 12345), UDPDiscoveryHandler)
    server.serve_forever()

def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    # start UPD discovery service
    Thread(target=startUDPDiscovery).start()

    # TODO use argparse
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])

    server = TCPServer((host, port), RequestHandler)
    logging.info("Listening on {}:{}".format(host, port))

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logging.debug("Server loop running in thread: " + server_thread.name)

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass

    logging.info("Server shutting down...")
    server.shutdown()
    server.server_close()
    logging.info("Bye!")

if __name__ == '__main__':
    main()
