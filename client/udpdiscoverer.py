import logging, socket, time

class UDPDiscoverer:

	def __init__(self):
		timeout = 5

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
		sock.settimeout(timeout)

		sock.sendto("I_NEED_A_BATTLESHIP_PLUS_PLUS_SERVER".encode("UTF-8"), ("<broadcast>", 12345))

		try:
			stopTime = time.time() + timeout
			while time.time() < stopTime:
				data, addr = sock.recvfrom(1024)
				if data.decode("UTF-8") == "I_AM_A_BATTLESHIP_PLUS_PLUS_SERVER":
					logging.debug("Found server at %s:%s" % (addr[0], addr[1]))
		except socket.timeout:
			print("No servers found.")

		sock.close()
