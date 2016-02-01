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

            self.__msgtype, self.__msgparams = self.__msgparser.decode(msg.decode())
            logging.debug("Msg type: " + self.__msgtype)

            # switch message types
            if self.__msgtype == 'game_create':
                report = self.__create_game()
            elif self.__msgtype == 'game_join':
                report = self.__join_game()
            else:
                report = self.__unknown_msg()

            # send answer to client
            self.request.sendall(report)

    def __create_game(self):
        # make sure parameter list is complete
        report = self.__expect_parameter(['name'])
        if report:
            return report

        # create game and make sure that the lobby name is unique
        if self.__lobby_model.add_lobby(self.__msgparams['name']):
            # lobby name was unique
            # Successful_Game_Create
            report = self.__msgparser.encode('report', {'status': '28'})
        else:
            # lobby name already exists
            # Illegal_Game_Definition
            report = self.__msgparser.encode('report', {'status': '37'})
        return report

    def __join_game(self):
        # make sure parameter list is complete
        report = self.__expect_parameter(['name'])
        if report:
            return report

        # join game and make sure that the lobby name exists
        if self.__lobby_model.join_lobby(self.__msgparams['name']):
            # Successful_Game_Join
            report = self.__msgparser.encode('report', {'status': '27'})
        else:
            # Illegal_Game_Definition
            report = self.__msgparser.encode('report', {'status': '37'})
        return report

    def __unknown_msg(self):
        logging.warning("Unknown msg type.")
        # Message_Not_Recognized
        report = self.__msgparser.encode('report', {'status': '40'})
        return report

    def __expect_parameter(self, params):
        for p in params:
            if not self.__msgparams[p]:
                logging.warning("Malformed msg. Missing parameter: " + p)
                # Message_Not_Recognized
                report = self.__msgparser.encode('report', {'status': '40'})
                return report
        return None
