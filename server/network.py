class ForkingTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass
