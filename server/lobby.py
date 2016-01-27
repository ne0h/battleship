import logging
import socketserver
import struct
import threading

from messageparser import *

#logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

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

            # switch message types
            if msgtype == 'game_create':

                # check if parameter list is complete
                if not msgparams['name']:
                    logging.warning("Malformed msg.")
                    # Message_Not_Recognized
                    report = self.__msgparser.encode('report', {'status': '40'})
                else:
                    # try to add lobby and make sure that the name is unique
                    if self.__add_lobby(msgparams['name']):
                        # lobby name was unique
                        # Successful_Game_Create
                        report = self.__msgparser.encode('report', {'status': '28'})
                    else:
                        # lobby name already exists
                        # Illegal_Game_Definition
                        report = self.__msgparser.encode('report', {'status': '37'})

                # send answer to client
                self.request.sendall(report)
            else:
                logging.warning("Unknown msg type.")
                # Message_Not_Recognized
                report = self.__msgparser.encode('report', {'status': '40'})

    def __add_lobby(self, name):
        result = True
        lock = threading.Lock()
        lock.acquire()
        logging.debug('__lobby_list.count(name) ' + str(self.__lobby_list.count(name)))
        logging.debug('__lobby_list ' + str(self.__lobby_list))
        if self.__lobby_list.count(name) > 0:
            result = False
        else:
            logging.debug('Trying to append {} to __lobby_list'.format(name))
            self.__lobby_list.append(name)
        lock.release()
        return result
