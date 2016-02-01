import threading
import logging

# list of existing lobby names
global_lobby_list = []

# list of ongoing games
global_game_list = []

# set of lobby update callbacks
global_on_lobby_update_callbacks = set()

# locks for all the lists above
global_lobby_list_lock = threading.Lock()
global_game_list_lock = threading.Lock()
global_on_lobby_update_callbacks_lock = threading.Lock()

class Lobby:
    """
    Lobby Model
    """

    def add_lobby(self, name):
        """
        Create a new lobby and make sure that the name is unique.
        Return True on success and False on failure (i.e., lobby name was already taken).
        """
        global global_lobby_list
        global global_lobby_list_lock
        result = True
        global_lobby_list_lock.acquire()
        if global_lobby_list.count(name) > 0:
            result = False
        else:
            global_lobby_list.append(name)
            self.notify_lobby_update()
        global_lobby_list_lock.release()
        return result

    def join_lobby(self, name):
        """
        Join an existing lobby.
        Return True on success and False on failure (i.e., lobby name does not exist).
        """
        global global_lobby_list
        global global_lobby_list_lock
        result = True
        global_lobby_list_lock.acquire()
        if global_lobby_list.count(name) > 0:
            g = Game(name)
            global_game_list.append(g)
            self.notify_lobby_update()
        else:
            result = False
        global_lobby_list_lock.release()
        return result

    def register_on_lobby_update_callback(self, callback):
        """
        Register a callback function that will be called by the Model as soon as a lobby update occurs.
        """
        global global_on_lobby_update_callbacks
        global global_on_lobby_update_callbacks_lock
        global_on_lobby_update_callbacks_lock.acquire()
        global_on_lobby_update_callbacks.add(callback)
        global_on_lobby_update_callbacks_lock.release()
        logging.debug("register_on_lobby_update_callback() called")

    def notify_lobby_update(self):
        global global_on_lobby_update_callbacks
        global global_on_lobby_update_callbacks_lock
        global_on_lobby_update_callbacks_lock.acquire()
        for cb in global_on_lobby_update_callbacks:
            cb()
        global_on_lobby_update_callbacks_lock.release()
