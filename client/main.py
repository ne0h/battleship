import argparse, sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../common'))

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging

from view import MainForm
from backend import Backend

def setupArgparse():
	parser = argparse.ArgumentParser(description="Battleship++ Client Application")
	parser.add_argument("--host", metavar=("<HOSTNAME>", "<PORT>"),	help="Connect directly without settings dialog.",
			nargs=2, type=str)

	return parser

if __name__ == "__main__":
	"""
	Starts the game client.
	"""
	fieldLength = 16

	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
	logging.info("Starting client...")

	args = setupArgparse().parse_args()
	hostname = None
	port = None
	if args.host:
		if not args.host[1].isdigit():
			logging.error("Wrong connection settings. Not connected so far.")
		else:
			hostname = args.host[0]
			port = int(args.host[1])

	backend = Backend(fieldLength, hostname, port)

	app = QApplication(sys.argv)
	screen = MainForm(backend, fieldLength)
	screen.show()
	sys.exit(app.exec_())
