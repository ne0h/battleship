import sys
sys.path.append("../common")

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging

from view import MainForm
from backend import Backend

if __name__ == '__main__':
	"""
	Starts the game client.
	"""

	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
	logging.info("Starting client...")

	fieldLength = 16

	app = QApplication(sys.argv)
	screen = MainForm(Backend(fieldLength), fieldLength)
	screen.show()
	sys.exit(app.exec_())
