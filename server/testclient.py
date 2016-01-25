from socket import *

host = '127.0.0.1'
port = 44444

def b():
    """
    Helper function to convert to byte-string, because I'm too lazy to type all this.
    """
    encode(encoding='UTF-8')

def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    data = ''
    while data != '/quit':
        data = input('> ')
        sock.send(b"foobar")

if __name__ == '__main__':
    main()
