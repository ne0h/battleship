import playingfield
import logging
from enum import Enum
import threading

# all the callback shit
class GameEvent(Enum):
    on_ship_edit = 1,
    on_game_start = 2,
    on_attack = 3,
    on_host_begins = 4,
    on_guest_begins = 5

callbacks = {}
callbacks[GameEvent.on_ship_edit] = []
callbacks[GameEvent.on_game_start] = []
callbacks[GameEvent.on_host_begins] = []
callbacks[GameEvent.on_guest_begins] = []
callbacks[GameEvent.on_attack] = []

callbacks_lock = threading.Lock()

class GameStatus(Enum):
    waiting = 1,
    ready = 2,
    ongoing = 3


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
        from random import randint
        self.__turn = randint(1,2)

    def set_second_player(self, id):
        self.__second_player = id
        self.__status = GameStatus.ready

    def remove_second_player(self):
        self.__second_player = None
        self.__status = GameStatus.waiting

    def get_turn(self):
        return self.__turn

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def is_waiting(self):
        return self.__status == GameStatus.waiting

    def start(self):
        if self.__status is not GameStatus.ongoing:
            return

        if self.__turn == 1:
            self.__notify_all(GameEvent.on_host_begins)
        else:
            self.__notify_all(GameEvent.on_guest_begins)

    def get_player(self, player):
        if player == 1:
            return self.__first_player
        elif player == 2:
            return self.__second_player
        return False

    def place_ship(self, player, x, y, direction, id):
        bow, rear = self.__x_y_direction_id_to_bow_rear(x, y, direction, id)

        logging.debug('place_ship x:{} y:{} dir:{} id:{} --> bow.x:{} bow.y:{} rear.x:{} rear.y:{}'.format(x, y, direction, id, bow.x, bow.y, rear.x, rear.y))

        suc, left = self.__get_field_by_player(player).placeShip(bow, rear)

        # trigger on_game_start if ship placement is done
        if self.__is_game_preparation_done():
            self.__status = GameStatus.ongoing
            self.__notify_all(GameEvent.on_game_start)

        return suc, left

    def move_ship(self, player, id, direction):
        field = self.__get_field_by_player(player)
        logging.debug('move_ship()')

    def fire(self, player, x, y):
        logging.debug('fire()')
        result, updated = self.__get_field_by_player(player).attack(playingfield.Field(x, y))
        if result == playingfield.FieldStatus.WATER:
            condition = 'free'
        elif result == playingfield.FieldStatus.DAMAGEDSHIP:
            condition = 'damaged'
        else:
            logging.debug("attack() returns invalid condition: {}".format(repr(result)))
            condition = None
        # trigger on_attack event
        if updated:
            self.__next_turn()
            params = {
                'x': x,
                'y': y,
                'condition': condition
            }
            self.__notify_all(GameEvent.on_attack, params)
        return condition, updated

    def nuke(self, player, x, y):
        field = self.__get_field_by_player(player)
        logging.debug('nuke()')

    def just_begin_ship_placement_already(self):
        # this is bullshit
        self.__notify_all(GameEvent.on_ship_edit)

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

    def __next_turn(self):
        # toggle between 1 and 2
        self.__turn = 3 - self.__turn

    def __get_field_by_player(self, player):
        if player == 1:
            return self.__first_field
        elif player == 2:
            return self.__second_field
        return None

    def __is_game_preparation_done(self):
        return not (self.__first_field.moreShipsLeftToPlace() or self.__second_field.moreShipsLeftToPlace())

    def __x_y_direction_id_to_bow_rear(self, x, y, direction, id):
        if id == 0:
            length = 5
        elif 1 <= id <= 2:
            length = 4
        elif 3 <= id <= 5:
            length = 3
        elif 6 <= id <= 9:
            length = 2

        bow = playingfield.Field(x, y)
        rear = None

        if direction == "N":
            rear = playingfield.Field(x, y + (length - 1))
        elif direction == "S":
            rear = playingfield.Field(x, y - (length - 1))
        elif direction == "E":
            rear = playingfield.Field(x + (length - 1), y)
        elif direction == "W":
            rear = playingfield.Field(x - (length - 1), y)
        else:
            logging.debug("Weird board init direction received: {}".format(direction))

        return bow, rear

    def __notify_all(self, event, params = {}):
        logging.debug("Game __notify_all({})".format(event))
        global callbacks
        callbacks_lock.acquire()
        for cb in callbacks[event]:
            cb(**params)
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
