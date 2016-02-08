import threading
import logging
from enum import Enum
from game import *

class LobbyError(Enum):
    game_is_full = 1,
    game_does_not_exist = 2

class LobbyEvent(Enum):
    on_update = 1

global_games = {}
global_waiting_games = set()
global_players = []
global_callbacks = {}
global_callbacks[LobbyEvent.on_update] = []

global_games_lock = threading.Lock()
global_players_lock = threading.Lock()
global_callbacks_lock = threading.Lock()


class LobbyModel:

    def add_lobby(self, name, playerid):
        """
        Create a new lobby and make sure that the name is unique.
        Return the new game on success and False on failure (i.e., lobby name was already taken).
        """
        global global_games
        global global_waiting_games
        global global_players
        global global_games_lock
        global global_players_lock
        global_games_lock.acquire()

        if name in global_games:
            global_games_lock.release()
            return False

        # TODO wtf is this
        global_players_lock.acquire()
        global_games[name] = Game(name)
        global_games[name].get_player(1).set_id(playerid)
        global_players.append(playerid)
        global_players_lock.release()

        global_waiting_games.add(name)
        global_games_lock.release()
        self.__notify_all(LobbyEvent.on_update)
        return global_games[name]

    def join_lobby(self, name, playerid):
        """
        Join an existing lobby.
        Return True on success and False on failure as first return parameter.
        Return the joined game on success and an error type on failure as second return parameter.
        """
        global global_games
        global global_waiting_games
        global global_games_lock
        global_games_lock.acquire()

        if name not in global_games:
            global_games_lock.release()
            return False, LobbyError.game_does_not_exist

        if name not in global_waiting_games:
            global_games_lock.release()
            return False, LobbyError.game_is_full

        global_waiting_games.remove(name)
        global_games[name].get_player(2).set_id(playerid)
        global_players_lock.acquire()
        global_players.remove(playerid)
        global_players_lock.release()
        global_games_lock.release()
        self.__notify_all(LobbyEvent.on_update)
        return True, global_games[name]

    def get_number_of_games(self):
        global global_games
        global global_waiting_games
        return len(global_games), len(global_waiting_games)

    def get_number_of_players(self):
        global global_games
        global global_waiting_games
        return 2 * len(global_games) - len(global_waiting_games)

    def get_player_ids(self):
        global global_players
        global global_players_lock

        global_players_lock.acquire()

        # TODO do I need to do a copy here
        result = []
        for p in global_players:
            result.append(p)

        global_players_lock.release()
        return result

    def get_games_info(self):
        global global_games
        global global_waiting_games
        global global_games_lock
        global_games_lock.acquire()

        result = []
        for _, g in global_games.items():
            # get number of players
            if g.get_name() in global_waiting_games:
                number_of_players = 1
            else:
                number_of_players = 2
            result.append({
                'game_name': g.get_name(),
                'number_of_players': number_of_players,
                'nicknames': [g.get_player(1).get_nick(), g.get_player(2).get_nick()],
                'ids': [g.get_player(1).get_id(), g.get_player(2).get_id()]
            })

        global_games_lock.release()
        return result

    def register_callback(self, event, callback):
        """
        Register a callback that will be triggered as a given event occurs.
        """
        logging.debug("register_callback({})".format(event))
        global global_callbacks
        global global_callbacks_lock
        global_callbacks_lock.acquire()
        global_callbacks[event].append(callback)
        global_callbacks_lock.release()

    def remove_callback(self, event, callback):
        """
        Remove a callback.
        """
        logging.debug("remove_callback({})".format(event))
        global global_callbacks
        global global_callbacks_lock
        global_callbacks_lock.acquire()
        global_callbacks[event].remove(callback)
        global_callbacks_lock.release()

    def __notify_all(self, event):
        logging.debug("__notify_all({})".format(event))
        global global_callbacks
        for cb in global_callbacks[event]:
            cb()
