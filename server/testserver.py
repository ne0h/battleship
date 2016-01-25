import socketserver

host = '127.0.0.1'
port = 44444
buffsize = 1024

class TestRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.client_address[0])
        print(self.data)
        self.request.sendall(self.data)

class ForkingTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ForkingTCPServer((host, port), TestRequestHandler)
    server.serve_forever()

    # sock = socket(AF_INET, SOCK_STREAM)
    # sock.bind((host, port))
    # sock.listen()
    # print("listening on {}:{}".format(host, port))
    # conn, addr = sock.accept()
    # print("connection from {}".format(addr))
    # while 1:
    #     data = conn.recv(buffsize)
    #     if not data:
    #         break
    #     print(data)
    #     conn.send(data)
    # conn.close()

if __name__ == '__main__':
    main()
