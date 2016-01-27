import threading

global_lobby_list = []

class Lobby:
    """
    Lobby Model
    """

    def add_lobby(self, name):
        """
        Create a new lobby and make sure that the name is unique.
        Return True on success and False on failure (i.e., lobby name was already taken)
        """
        result = True
        lock = threading.Lock()
        lock.acquire()
        global global_lobby_list
        if global_lobby_list.count(name) > 0:
            result = False
        else:
            global_lobby_list.append(name)
        lock.release()
        return result
