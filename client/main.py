import argparse, sys, os, wave

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../common"))

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging

from view import MainForm
from backend import Backend

def setupArgparse():
	parser = argparse.ArgumentParser(description="Battleship++ Client Application")
	parser.add_argument("-c", "--connect", metavar=("<HOSTNAME>", "<PORT>"),
						help="Connect directly without settings dialog.", nargs=2, type=str)
	parser.add_argument('-d', '--devmode', help="Dev mode.", action='store_true')
	parser.add_argument('-n', '--nick', help="Nickname.")

	return parser

if __name__ == "__main__":
	"""
	Starts the game client.
	"""

	import os
	path = "%s/sounds/attack.wav" % os.path.join(os.path.dirname(os.path.realpath(__file__)))


	fieldLength = 16

	logging.basicConfig(format="%(asctime)s - CLIENT - %(levelname)s - %(message)s", level=logging.DEBUG)
	logging.info("Starting client...")

	args = setupArgparse().parse_args()

	devmode = args.devmode
	hostname = None
	port = None
	nickname = args.devmode
	if nickname is None:
		nickname = "BOFH"
	if args.connect:
		if not args.connect[1].isdigit():
			logging.error("Wrong connection settings. Not connected so far.")
		else:
			hostname = args.connect[0]
			port = int(args.connect[1])
			nickname = args.nick

	backend = Backend(fieldLength, hostname, port, nickname, devmode)

	app = QApplication(sys.argv)
	screen = MainForm(backend, fieldLength, devmode)
	screen.show()
	sys.exit(app.exec_())
