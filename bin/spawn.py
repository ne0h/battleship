#!/usr/bin/env python

import os, sys, argparse, threading, logging
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../server'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../common'))
import server

def spawn_server():
    for port in range(33333, 44444):
        try:
            serv = server.TCPServer(('localhost', port), server.RequestHandler)
            serv_thread = threading.Thread(target=serv.serve_forever)
            serv_thread.daemon = True
            serv_thread.start()
            logging.info("Server running in thread: {}".format(serv_thread.name))
            return serv, port
        except OSError as e:
            logging.debug("Port {} in use. Skipping.".format(str(port)))

def main():
    logging.basicConfig(format="%(asctime)s - SERVER - %(levelname)s - %(message)s", level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, default=2)
    parser.add_argument('-d', '--devmode', help="Dev mode.", action='store_true')
    args = parser.parse_args()
    n = args.number
    devmode = args.devmode

    # spawn server and get final port that the server is listening on
    serv, port = spawn_server()
    logging.info("Server is now listening on port {}.".format(str(port)))

    # spawn clients
    for x in range(n):
        cmd = 'python3 {}{} --connect localhost {} --nick {}'.format(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../client/main.py'), ' --devmode' if devmode else '', str(port), 'Player' + str(x))
        logging.info("Spawn client #{}: ".format(str(x), cmd))
        t = threading.Thread(target = lambda: os.system(cmd))
        t.daemon = True
        t.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass

    # shutdown server
    logging.info("Server shutting down...")
    serv.shutdown()
    serv.server_close()
    logging.info("Bye!")

if __name__ == '__main__':
    main()
