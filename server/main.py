#!/usr/bin/env python

import os
import sys
import logging

sys.path.append("../common")

from lobby import *

def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    if len(sys.argv) != 3:
        logging.error("Invalid number of arguments.")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])

    lobby = LobbyTCPServer((host, port), LobbyRequestHandler)
    logging.info("Listening on {}:{}".format(host, port))

    lobby.serve_forever()

if __name__ == '__main__':
    main()
