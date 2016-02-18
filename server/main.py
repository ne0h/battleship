#!/usr/bin/env python

import os
import sys
import logging
import threading
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../common'))
from server import *
from socketserver import UDPServer, BaseRequestHandler


class UDPDiscoveryHandler(BaseRequestHandler):

    def handle(self):
        if self.request[0].decode("UTF-8") == "I_NEED_A_BATTLESHIP_PLUS_PLUS_SERVER":
            socket = self.request[1]
            socket.sendto("I_AM_A_BATTLESHIP_PLUS_PLUS_SERVER".encode("UTF-8"), self.client_address)

def main():
    logging.basicConfig(format="%(asctime)s - SERVER - %(levelname)s - %(message)s", level=logging.DEBUG)

    # parse host and port args
    parser = argparse.ArgumentParser(description="battleshit++ server")
    parser.add_argument('host')
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    # start UPD discovery service
    udpdiscovery_server = UDPServer(("", 12345), UDPDiscoveryHandler)
    udpdiscovery_server_thread = threading.Thread(target=udpdiscovery_server.serve_forever)
    udpdiscovery_server_thread.daemon = True
    udpdiscovery_server_thread.start()
    logging.debug("UDP discovery server running in thread: " + udpdiscovery_server_thread.name)

    server = TCPServer((args.host, args.port), RequestHandler)
    logging.info("Listening on {}:{}".format(args.host, args.port))

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
    udpdiscovery_server.shutdown()
    udpdiscovery_server.server_close()
    logging.info("Bye!")

if __name__ == '__main__':
    main()
