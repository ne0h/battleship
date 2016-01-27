import logging
import socketserver
import struct
import threading

from messageparser import *

class LobbyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class LobbyRequestHandler(socketserver.BaseRequestHandler):
    """
    Handle lobby requests.

    Args:
        - lobby_list
    """

    def setup(self):
        self.__lobby_list = []
        self.__msgparser = MessageParser()

    def handle(self):
        # receive header (first 2 bytes) which represent the number of bytes that follow
        size = self.request.recv(2)
        if not size:
            logging.error("Invalid size field in header.")
        else:
            size = struct.unpack('>H', size)[0]
            logging.debug("header = " + str(size))
            logging.info("Client address: " + self.client_address[0])

            msg = self.request.recv(size)
            logging.debug(b"Data: " + msg)

            msgtype, msgparams = self.__msgparser.decode(msg.decode())
            logging.debug("Msg type: " + msgtype)
            if msgtype == 'game_create':
                # check if parameter list is complete
                if not msgparams['name']:
                    logging.warning("Malformed msg.")
                else:
                    # check if lobby is unique
                    if self.__add_lobby(msgparams['name']):
                        # success report
                        report = self.__msgparser.encode('report', {'status': '28'})
                    else:
                        # error report
                        report = self.__msgparser.encode('report', {'status': '37'})
                    self.request.sendall(report)
            else:
                logging.warning("Unknown msg type.")

    def __add_lobby(self, name):
        result = True
        lock = threading.Lock()
        lock.acquire()
        if self.__lobby_list.count(name) > 0:
            result = False
        else:
            self.__lobby_list.append(name)
        lock.release()
        return result
