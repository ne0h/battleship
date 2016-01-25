from socket import *

class Connection:
    """
    A server connection.

    Args:
        socket -- the tcp socket object that is used to accept incoming connections
    """
    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
