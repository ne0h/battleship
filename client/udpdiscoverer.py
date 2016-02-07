import logging, socket, time
from threading import Thread

class UDPDiscoverer:

	def __run(self):
		timeout = 2
		run = True

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
		sock.settimeout(timeout)

		while run:
			sock.sendto("I_NEED_A_BATTLESHIP_PLUS_PLUS_SERVER".encode("UTF-8"), ("<broadcast>", 12345))
			try:
				stopTime = time.time() + timeout
				while time.time() < stopTime:
					data, addr = sock.recvfrom(1024)
					if data.decode("UTF-8") == "I_AM_A_BATTLESHIP_PLUS_PLUS_SERVER":
						logging.debug("Found server at %s:%s" % (addr[0], addr[1]))
						self.__backend.udpDiscoveryUpdate(addr[0])
			except socket.timeout:
				print("No servers found.")

		sock.close()

	def close(self):
		run = False

	def __init__(self, backend):
		self.__backend = backend
		
		Thread(target=self.__run).start()