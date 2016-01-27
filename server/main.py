#!/usr/bin/env python

import os
import sys
import logging
import threading

sys.path.append("../common")

from lobby import *

USAGE = "Usage: main.py <host> <port>"

def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])

    lobby = LobbyTCPServer((host, port), LobbyRequestHandler)
    logging.info("Listening on {}:{}".format(host, port))

    lobby_thread = threading.Thread(target=lobby.serve_forever)
    lobby_thread.daemon = True
    lobby_thread.start()
    logging.info("Server loop running in thread: " + lobby_thread.name)

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass

    logging.info("Server shutting down...")
    lobby.shutdown()
    lobby.server_close()
    logging.info("Bye!")

if __name__ == '__main__':
    main()
