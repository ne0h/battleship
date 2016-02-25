import sys
import logging
import socketserver
import struct
import threading
import hashlib
from messageparser import MessageParser
import messages
from lobby import *
from game import *
from helpers import *


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.__client = ClientHandler(self.request)

    def handle(self):
        self.__client.handle()

    def finish(self):
        self.__client.finish()


class ClientHandler:

    def __init__(self, sock):
        self.__socket = sock
        self.__message_parser = MessageParser()
        self.__lobby_model = LobbyModel()
        # name of the game
        self.__game = None
        # player number (1 or 2)
        self.__player = None
        # player id lol
        self.__id = self.__get_own_player_id()
        # add client as player
        self.__lobby_model.add_player(self.__id)

        # register callbacks
        # TODO consistently rename on_update into on_update_lobby
        self.__lobby_model.register_callback(LobbyEvent.on_update, self.on_update_lobby)
        self.__lobby_model.register_callback(LobbyEvent.on_game_deleted, self.on_game_deleted)

    def handle(self):
        logging.info("Client {} connected.".format(self.__socket.getpeername()))
        while True:
            # receive 2 bytes size header
            size = self.__socket.recv(2)
            if not size:
                logging.debug("Did not receive 2 bytes header.")
                break
            size = struct.unpack('>H', size)[0]
            logging.debug("Size: " + str(size))

            # receive message body
            msg = self.__socket.recv(size)
            if not msg:
                logging.debug("Did not receive {} bytes body.".format(str(size)))
                break
            logging.debug(b"Raw in: " + msg)

            # explode received data into message type and parameters
            msgtype, msgparams = self.__message_parser.decode(msg.decode())
            logging.debug("Msg type: " + msgtype)
            logging.debug("Msg parameters: " + repr(msgparams))

            # dispatch message type
            if msgtype == messages.CREATE_GAME:
                self.__create_game(msgparams)
            elif msgtype == messages.JOIN_GAME:
                self.__join_game(msgparams)
            elif msgtype == messages.SET_NICK:
                self.__set_nickname(msgparams)
            elif msgtype == messages.LEAVE_GAME:
                self.__leave_game()
            elif msgtype == messages.INIT_BOARD:
                self.__init_board(msgparams)
            elif msgtype == messages.FIRE:
                self.__fire(msgparams)
            elif msgtype == messages.NUKE:
                self.__nuke(msgparams)
            elif msgtype == messages.MOVE:
                self.__move(msgparams)
            elif msgtype == messages.SURRENDER:
                self.__surrender()
            elif msgtype == messages.CHAT_SEND:
                self.__chat()
            else:
                self.__unknown_msg()

    #
    # Callbacks
    #

    def on_update_lobby(self):
        logging.debug("on_update_lobby()")

        # Get required data for update lobby msg
        number_of_clients = self.__lobby_model.get_number_of_players()
        number_of_games = self.__lobby_model.get_number_of_games()
        games_info = self.__lobby_model.get_games_info()
        players_info = self.__lobby_model.get_players_info()

        # Update_Lobby
        data = {
            'status': 16,
            'number_of_clients': number_of_clients,
            'number_of_games': number_of_games[0]
        }

        i = 0
        weirdkey = 'game_name_{}'
        moreweirdkeys = 'game_players_count_{}'
        whatevenisthis = 'game_player_{}_{}'
        waitwhat = 'player_name_{}'
        yetanotherkey = 'player_identifier_{}'

        for game in games_info:
            # game stuff
            data[weirdkey.format(i)] = game['game_name']
            data[moreweirdkeys.format(i)] = game['number_of_players']
            # player 1 stuff
            data[whatevenisthis.format(i, 0)] = game['ids'][0]
            # player 2 stuff
            if game['number_of_players'] == 2:
                data[whatevenisthis.format(i, 1)] = game['ids'][1]
            i += 1

        i = 0
        for player in players_info:
            # player stuff
            data[yetanotherkey.format(i)] = player['id']
            data[waitwhat.format(i)] = player['nickname']
            i += 1

        msg = self.__message_parser.encode('report', data)
        self.__send(msg)

    def on_game_deleted(self):
        self.__game = None
        self.__send(self.__message_parser.encode('report', {'status': '19'}))

    def on_game_ended(self, winner, id0, id1):
        self.__game = None
        msg = {
            'status': '17',
            'winner': winner - 1,
            'name_of_game': self.__game,
            'identifier_0': id0,
            'identifier_1': id1,
            'reason_for_game_end': 'Because of reasons.'
        }
        self.__send(self.__message_parser.encode('report', msg))

    def on_ship_edit(self):
        logging.debug('on_ship_edit()')
        self.__send(self.__message_parser.encode('report', {'status': '18'}))

    def on_game_start(self):
        logging.debug('on_game_start()')
        self.__send(self.__message_parser.encode('report', {'status': '48'}))

    def on_host_begins(self):
        logging.debug('on_host_begins()')
        self.__begin_turn()

    def on_guest_begins(self):
        logging.debug('on_guest_begins()')
        self.__begin_turn()

    def on_attack(self, x, y, condition):
        logging.debug('on_attack()')
        msg = None
        # if player is enemy
        if self.__lobby_model.get_game(self.__game).get_turn() == self.__player:
            # update own field
            msg = {
                'status': 13,
                'was_special_attack': 'false',
                'coordinate_x': x,
                'coordinate_y': y
            }
            self.__send(self.__message_parser.encode('report', msg))
            # trigger next turn wtf
            self.__begin_turn()
        else:
            # update enemy field
            msg = {
                'status': 14,
                'number_of_updated_fields': '1',
                'field_0_x': x,
                'field_0_y': y,
                'field_0_condition': condition
            }
            self.__send(self.__message_parser.encode('report', msg))

    def on_special_attack(self, x, y, updates):
        logging.debug('on_special_attack()')
        msg = None
        if self.__lobby_model.get_game(self.__game).get_turn() == self.__player:
            # update own field
            msg = {
                'status': 13,
                'was_special_attack': 'true',
                'coordinate_x': x,
                'coordinate_y': y
            }
            self.__send(self.__message_parser.encode('report', msg))
            # trigger next turn wtf
            self.__begin_turn()
        else:
            # update enemy field
            msg = {
                'status': 14,
                'number_of_updated_fields': len(updates)
            }
            i = 0
            for j in updates:
                msg['field_{}_x'.format(i)] = j['field'].x
                msg['field_{}_y'.format(i)] =j['field'].y
                msg['field_{}_condition'.format(i)] = j['status']
                i += 1
            self.__send(self.__message_parser.encode('report', msg))

    def on_move(self, updates):
        logging.debug('on_move()')
        msg = None
        if self.__lobby_model.get_game(self.__game).get_turn() == self.__player:
            # update enemy field
            if len(updates) > 0:
                msg = {
                    'status': 14,
                    'number_of_updated_fields': len(updates)
                }
                i = 0
                for j in updates:
                    msg['field_{}_x'.format(i)] = j['field'].x
                    msg['field_{}_y'.format(i)] =j['field'].y
                    msg['field_{}_condition'.format(i)] = j['status']
                    i += 1
                self.__send(self.__message_parser.encode('report', msg))
            # trigger next turn wtf
            self.__begin_turn()

    def get_socket(self):
        return self.__socket

    def finish(self):
        logging.info("Client disconnected.")

        # remove any left callbacks
        self.__lobby_model.remove_callback(LobbyEvent.on_update, self.on_update_lobby)
        self.__lobby_model.remove_callback(LobbyEvent.on_game_deleted, self.on_game_deleted)

        # remove player from lobby
        self.__lobby_model.delete_player(self.__id)

    def __create_game(self, params):
        # make sure parameter list is complete
        if not self.__expect_parameter(['name'], params):
            return

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            # 31 is the new 42
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # check game name length
        if 1 > len(params['name']) or len(params['name']) > 64:
            logging.debug("Game name too long.")
            self.__send(self.__message_parser.encode('report', {'status': '37'}))
            return

        # create the game
        game = self.__lobby_model.add_lobby(params['name'], self.__id)

        if not game:
            self.__send(self.__message_parser.encode('report', {'status': '37'}))
            return

        self.__game = params['name']
        self.__player = 1
        self.__send(self.__message_parser.encode('report', {'status': '28'}))

        # register game callbacks
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_ship_edit, self.on_ship_edit)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_start, self.on_game_start)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_attack, self.on_attack)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_special_attack, self.on_special_attack)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_move, self.on_move)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_host_begins, self.on_host_begins)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_ended, self.on_game_ended)

    def __join_game(self, params):
        # make sure parameter list is complete
        if not self.__expect_parameter(['name'], params):
            return

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # join the game
        game, e = self.__lobby_model.join_lobby(params['name'], self.__id)

        # handle game join errors
        if e:
            if e == LobbyError.game_is_full:
                self.__send(self.__message_parser.encode('report', {'status': '47'}))
                return
            elif e == LobbyError.game_does_not_exist:
                self.__send(self.__message_parser.encode('report', {'status': '37'}))
                return

        # ack game join
        self.__send(self.__message_parser.encode('report', {'status': '27'}))

        self.__game = params['name']
        self.__player = 2

        # register game callbacks
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_ship_edit, self.on_ship_edit)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_start, self.on_game_start)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_attack, self.on_attack)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_special_attack, self.on_special_attack)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_move, self.on_move)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_guest_begins, self.on_guest_begins)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_ended, self.on_game_ended)

        self.__lobby_model.get_game(self.__game).just_begin_ship_placement_already()

    def __set_nickname(self, params):
        if not self.__expect_parameter(['name'], params):
            return

        if len(params['name']) > 64:
            logging.debug("Nickname too long.")
            self.__send(self.__message_parser.encode('report', {'status': '36'}))
            return

        # tell lobby to set nickname and hope for the best
        self.__lobby_model.set_nickname(self.__id, params['name'])

    def __get_own_player_id(self):
        addr, port = self.__socket.getpeername()
        playerid = hashlib.sha1(b(addr + str(port))).hexdigest()
        return playerid

    def __init_board(self, params):
        logging.debug('__init_board()')

        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        shipx = 'ship_{}_x'
        shipy = 'ship_{}_y'
        shipdir = 'ship_{}_direction'

        # make sure that all parameters exist
        if not self.__expect_parameter(
            [shipx.format(i) for i in range(0, 10)] +
            [shipy.format(i) for i in range(0, 10)] +
            [shipdir.format(i) for i in range(0, 10)], params):
            return

        # init board
        left = True
        for id in range(0, 10):
            x = int(params[shipx.format(id)])
            y = int(params[shipy.format(id)])
            dir = params[shipdir.format(id)]
            logging.debug('self.__lobby_model :: {}'.format(repr(self.__lobby_model)))
            logging.debug('self.__lobby_model.get_game(self.__game) :: {}'.format(repr(self.__lobby_model.get_game(self.__game))))
            logging.debug('self.__game :: {}'.format(repr(self.__game)))
            suc, left = self.__lobby_model.get_game(self.__game).place_ship(self.__player, x, y, dir, id)

            # catch illegal placement
            if suc == -1:
                logging.debug("Nonsense ship placement.")
                self.__send(self.__message_parser.encode('report', {'status': '38'}))
                return

        if left:
            logging.debug("Something is still wrong with ship placement.")
            self.__send(self.__message_parser.encode('report', {'status': '38'}))
            return

        # ack init board
        self.__send(self.__message_parser.encode('report', {'status': '29'}))

        # trigger random begin return message
        self.__lobby_model.get_game(self.__game).start()

    def __leave_game(self):
        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        # if player who created game leaves then destroy the game else just leave
        #if self.__player == 1:
        #    self.__lobby_model.delete_game(self.__game)
        #else:
        #    self.__lobby_model.leave_game(self.__game)

        # make sure the game has started


        # nevermind lulz
        self.__lobby_model.delete_game(self.__game)

    def __fire(self, params):
        if not self.__expect_parameter(['coordinate_x', 'coordinate_y'], params):
            return

        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        # check if it's actually your turn
        if self.__lobby_model.get_game(self.__game).get_turn() != self.__player:
            self.__send(self.__message_parser.encode('report', {'status': '41'}))
            return

        # save move
        _, updated = self.__lobby_model.get_game(self.__game).fire(self.__player, params['coordinate_x'], params['coordinate_y'])
        if not updated:
            self.__send(self.__message_parser.encode('report', {'status': '39'}))
            return

        # successful attack
        self.__send(self.__message_parser.encode('report', {'status': '22'}))

        # check if game over
        self.__lobby_model.get_game(self.__game).check_if_game_over(self.__player)

    def __nuke(self, params):
        if not self.__expect_parameter(['coordinate_x', 'coordinate_y'], params):
            return

        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        # check if it's actually your turn
        if self.__lobby_model.get_game(self.__game).get_turn() != self.__player:
            self.__send(self.__message_parser.encode('report', {'status': '41'}))
            return

        # save move
        updated = self.__lobby_model.get_game(self.__game).nuke(self.__player, params['coordinate_x'], params['coordinate_y'])
        if len(updated) == 0:
            self.__send(self.__message_parser.encode('report', {'status': '32'}))
            return

        # successful special attack
        self.__send(self.__message_parser.encode('report', {'status': '24'}))

        # check if game over
        self.__lobby_model.get_game(self.__game).check_if_game_over(self.__player)

    def __move(self, params):
        if not self.__expect_parameter(['ship_id', 'direction'], params):
            return

        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        # check if it's actually your turn
        if self.__lobby_model.get_game(self.__game).get_turn() != self.__player:
            self.__send(self.__message_parser.encode('report', {'status': '41'}))
            return

        # save move
        result = self.__lobby_model.get_game(self.__game).move_ship(self.__player, int(params['ship_id']), params['direction'])
        if result is False:
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # successful move
        self.__send(self.__message_parser.encode('report', {'status': '21'}))

    def __surrender(self):
        # not in any game
        if self.__game is None:
            self.__send(self.__message_parser.encode('report', {'status': '43'}))
            return

        # surrender
        self.__lobby_model.get_game(self.__game).surrender(self.__player)

        # delete without triggering game aborted
        self.__lobby_model.delete_game(self.__game, aborted=False)

        # surrender accepted lol
        self.__send(self.__message_parser.encode('report', {'status': '23'}))

    def __begin_turn(self):
        self.__send(self.__message_parser.encode('report', {'status': '11'}))

    def __chat(self):
        # TODO implement chat
        self.__send(self.__message_parser.encode('report', {'status': '15'}))

    def __unknown_msg(self):
        self.__send(self.__message_parser.encode('report', {'status': '40'}))

    def __expect_parameter(self, expected, actual):
        keys = list(actual.keys())
        for p in expected:
            if p not in keys:
                self.__unknown_msg()
                return False
        return True

    def __send(self, msg):
        logging.debug(b"Raw out: " + msg)
        self.__socket.sendall(msg)
