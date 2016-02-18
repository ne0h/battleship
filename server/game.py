import playingfield
import logging
from enum import Enum
import threading

# all the callback shit
class GameEvent(Enum):
    on_ship_edit = 1,
    on_game_start = 2,
    on_update_field = 3

callbacks = {}
callbacks[GameEvent.on_ship_edit] = []
callbacks[GameEvent.on_game_start] = []
callbacks[GameEvent.on_update_field] = []

callbacks_lock = threading.Lock()

class GameStatus(Enum):
    waiting = 1,
    ready = 2


class Game:

    def __init__(self, name, id):
        """
        Create a new game.
        """
        self.__name = name
        self.__first_field = playingfield.PlayingField(16)
        self.__second_field = playingfield.PlayingField(16)
        self.__first_player = id
        self.__second_player = None
        self.__status = GameStatus.waiting
        # turn is either 1 or 2
        self.__turn = 1

    def set_second_player(self, id):
        self.__second_player = id
        self.__status = GameStatus.ready

    def remove_second_player(self):
        self.__second_player = None
        self.__status = GameStatus.waiting

    def get_turn(self):
        return self.__turn

    def next_turn(self):
        # toggle between 1 and 2
        self.__turn = 3 - self.__turn

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def is_waiting(self):
        return self.__status == GameStatus.waiting

    def get_player(self, player):
        if player == 1:
            return self.__first_player
        elif player == 2:
            return self.__second_player
        return False

    def place_ship(self, player, x, y, direction, id):
        logging.debug('place_ship()')

        bow, rear = self.__x_y_direction_id_to_bow_rear(x, y, direction, id)

        res = self.__get_field_by_player(player).placeShip(bow, rear)

        # trigger on_game_start if ship placement is done
        if self.__is_game_preparation_done():
            self.__notify_all(GameEvent.on_ship_edit)

        return res is not None

    def move_ship(self, player, id, direction):
        field = self.__get_field_by_player(player)
        logging.debug('move_ship()')

    def fire(self, player, x, y):
        field = self.__get_field_by_player(player)
        logging.debug('fire()')

    def nuke(self, player, x, y):
        field = self.__get_field_by_player(player)
        logging.debug('nuke()')

    def just_begin_ship_placement_already(self):
        # this is bullshit
        self.__notify_all(GameEvent.on_ship_edit)

    def __get_field_by_player(self, player):
        if player == 1:
            return self.__first_field
        elif player == 2:
            return self.__second_field
        return None

    def __is_game_preparation_done(self):
        # TODO
        pass

    def __x_y_direction_id_to_bow_rear(self):
        # TODO
        pass

    def register_callback(self, event, callback):
        """
        Register a callback that will be triggered as a given event occurs.
        """
        logging.debug("Game register_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].append(callback)
        callbacks_lock.release()

    def remove_callback(self, event, callback):
        """
        Remove a callback.
        """
        logging.debug("Game remove_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].remove(callback)
        callbacks_lock.release()

    def __notify_all(self, event):
        logging.debug("Game __notify_all({})".format(event))
        global callbacks
        callbacks_lock.acquire()
        for cb in callbacks[event]:
            cb()
        callbacks_lock.release()


class Player:

    def __init__(self, nick = None, id = None):
        self.__nick = nick
        self.__id = id

    def get_nick(self):
        return self.__nick

    def get_id(self):
        return self.__id

    def set_nick(self, nick):
        self.__nick = nick

    def set_id(self, id):
        self.__id = id
