#!/usr/bin/env python

import os
import sys
import logging
import threading
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../common'))
from server import *

USAGE = "Usage: main.py <host> <port>"

def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])

    server = TCPServer((host, port), RequestHandler)
    logging.info("Listening on {}:{}".format(host, port))

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logging.info("Server loop running in thread: " + server_thread.name)

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
