import logging
import socketserver
import struct
import threading

from messageparser import *
from lobby import *

class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.__lobby_model = Lobby()
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
                    if self.__lobby_model.add_lobby(msgparams['name']):
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
