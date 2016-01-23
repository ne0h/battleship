import abc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from playingfield import *

class ViewModel:

	def __init__(self):
		self.waitForShipPlacement = False
		self.newShipBow = None

class LobbyDialog(QDialog):

	def __joinGameOnClick(self):
		from backend import Callback

		gameId = self.__gamesWidget.currentItem().text().split(":")[0]
		cb = Callback()
		self.__backend.joinGameCallback(cb)

	def __createGameOnClick(self):
		pass

	def __setupGui(self):
		self.__statusLbl = QLabel()
		self.__gamesWidget = QListWidget()
		self.__gamesWidget.setSortingEnabled(True)
		self.__joinGameBtn = QPushButton("Join game")
		self.__joinGameBtn.clicked.connect(self.__joinGameOnClick)
		self.__createGameBtn = QPushButton("Create game")
		self.__createGameBtn.clicked.connect(self.__createGameOnClick)

		btnsLayout = QHBoxLayout()
		btnsLayout.addWidget(self.__joinGameBtn)
		btnsLayout.addWidget(self.__createGameBtn)
		btnsWgt = QWidget()
		btnsWgt.setLayout(btnsLayout)

		layout = QVBoxLayout()
		layout.addWidget(self.__statusLbl)
		layout.addWidget(self.__gamesWidget)
		layout.addWidget(btnsWgt)

		self.setLayout(layout)
		self.setWindowTitle("Lobby")
		self.resize(500, 300)
		self.show()

	def __onUpdateGamesList(self, players, games):
		self.__statusLbl.setText("%s players currently online and %s games are open!" % (len(players), len(games)))

		# only add new games
		for game in games:
			found = -1
			for i in range(0, self.__gamesWidget.count()):
				# this validation is sufficient, because colons are not allowed as values in the protocol
				if self.__gamesWidget.item(i).text().startswith("%s:" % (game.name)):
					found = i
					break;

			text = game.name
			if game.players[0] == "":
				text = ": %s" % ("An unnamed player")
			else:
				text = "%s: %s" % (text, game.players[0])
			if len(game.players) is 1:
				text = "%s is waiting for an oppenent" % (text)
			else:
				text = "%s vs. %s" % (text, game.players[1])

			# is there an update? if yes - update corresponding item
			# if not - add the new item
			if found is not -1:
				self.__gamesWidget.item(i).text = text
			else:
				self.__gamesWidget.addItem(text)
	
	def closeEvent(self, event):
		self.__backend.removeLobbyUpdateGamesCallback(self.__gamesListCb)

	def __init__(self, backend):
		from backend import Callback

		self.__backend = backend
		self.__gamesListCb = Callback()
		self.__gamesListCb.onAction = lambda players, games: self.__onUpdateGamesList(players, games)
		players, games = self.__backend.registerLobbyUpdateGamesCallback(self.__gamesListCb)

		super(LobbyDialog, self).__init__()
		self.__setupGui()
		self.__onUpdateGamesList(players, games)

class PlayingFieldWidget(QWidget):
	"""
	Shows a playing field.
	"""

	def _setupGui(self):
		self.setMaximumWidth(self._fieldSize  * 17 + 1)
		self.setMaximumHeight(self._fieldSize * 17 + 1)
		self.setStyleSheet("border: 1px solid red")

	@abc.abstractmethod
	def _getShips(self):
		pass

	def paintEvent(self, event):
		"""
		Paints the playing field when an event occurs.

		Args:
			event -- information about the event that occured
		"""

		painter = QPainter()
		painter.begin(self)
		self._drawPlayingField(painter)
		painter.end()

	def _drawPlayingField(self, painter):

		# fill each field with water
		for i in range(1, self._fieldLength + 1):
			for j in range(1, self._fieldLength + 1):
				painter.setBrush(QColor(0, 191, 255))
				painter.drawRect(i * self._fieldSize, j * self._fieldSize, self._fieldSize, self._fieldSize)

		# add ships
		painter.setBrush(QColor(210, 105, 30))
		for ship in self._getShips():

			# draw bow
			bow = ship.bow
			painter.drawPixmap((bow.x + 1) * self._fieldSize, (bow.y + 1) * self._fieldSize, self._fieldSize,
				self._fieldSize, QPixmap("./img/bow_" + ship.orientation.value + ".png"))
			
			# draw rear
			rear = ship.rear
			painter.drawPixmap((rear.x + 1) * self._fieldSize, (rear.y + 1) * self._fieldSize, self._fieldSize,
				self._fieldSize, QPixmap("./img/rear_" + ship.orientation.value + ".png"))
			
			# draw the rest
			for middle in ship.middles:
				painter.drawPixmap((middle.x + 1) * self._fieldSize, (middle.y + 1) * self._fieldSize, self._fieldSize,
					self._fieldSize, QPixmap("./img/middle_" + ship.orientation.value + ".png"))

		# draw horizontal and vertical enumeration
		painter.setPen(QColor(0, 0, 0))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(i*self._fieldSize, 0, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, str(i))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(0, i*self._fieldSize, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, chr(64 + i))

	def _mapClickToField(self, mouseEvent):
		x, y  = mouseEvent.x() // self._fieldSize, mouseEvent.y() // self._fieldSize		
		return Field(x - 1, y - 1)

	def __init__(self, backend, viewModel, fieldLength, fieldSize=25):
		self._viewModel = viewModel
		self._backend = backend
		self._fieldSize = fieldSize
		self._fieldLength = fieldLength

		super(PlayingFieldWidget, self).__init__()
		self._setupGui()

class OwnPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the user.
	"""

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent -- information about the mouse event
		"""

		fieldAddress = self._mapClickToField(mouseEvent)
		print("Click event at own field: %s" % (fieldAddress.toString()))

		if self._viewModel.waitForShipPlacement:
			if self._viewModel.newShipBow is None:
				self._viewModel.newShipBow = fieldAddress
			else:
				ship = self._backend.placeShip(fieldAddress, self._viewModel.newShipBow)

				self.repaint()
				self._viewModel.waitForShipPlacement = False
				self._viewModel.newShipBow = None

	def _getShips(self):
		return self._backend.getOwnShips()

	def __init__(self, backend, viewModel, fieldLength):
		PlayingFieldWidget.__init__(self, backend, viewModel, fieldLength)

class EnemeysPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the enemey.
	"""

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent -- information about the mouse event
		"""

		field = self._mapClickToField(mouseEvent)
		print("Click event at enemey's field: %s" % (field.toString()))

	def _getShips(self):
		return self._backend.getEnemeysShips()

	def __init__(self, backend, viewModel, fieldLength):
		PlayingFieldWidget.__init__(self, backend, viewModel, fieldLength)

class MainForm(QWidget):
	"""
	The main form that shows the complete user interface.
	"""

	def __startPlaceShip(self):
		self.__viewModel.waitForShipPlacement = True

	def __openLobby(self):
		import sys

		LobbyDialog(self.__backend).exec_()

	def __updateClientStatus(self):
		from backend import ClientStatus

		status = self.__backend.getClientStatus()

		if status is ClientStatus.NOGAMERUNNING:
			self.__statusLbl.setText("No game running, please use the lobby to connect to a game.")
		elif status is ClientStatus.PREPARATIONS:
			self.__statusLbl.setText("Please place your ships.")
		elif status is ClientStatus.OWNTURN:
			self.__status.setText("It is your turn.")
		elif status is ClientStatus.OPPONENTSTURN:
			self.__statusLbl.setText("Please wait for your opponent.")

	def __setupGui(self):

		# own playing field stuff
		ownPlayingFieldBox = QGroupBox("Your own playing field")
		ownPlayingFieldWgt = OwnPlayingFieldWidget(self.__backend, self.__viewModel, self.__fieldLength)
		ownPlayingFieldLayout = QVBoxLayout()
		ownPlayingFieldLayout.addWidget(ownPlayingFieldWgt)
		ownPlayingFieldBox.setLayout(ownPlayingFieldLayout)

		# enemies playing field stuff
		enemeysPlayingFieldBox = QGroupBox("Your enemey's playing field")
		enemeysPlayingFieldWgt = EnemeysPlayingFieldWidget(self.__backend, self.__viewModel, self.__fieldLength)
		enemiesPlayingFieldLayout = QVBoxLayout()
		enemiesPlayingFieldLayout.addWidget(enemeysPlayingFieldWgt)
		enemeysPlayingFieldBox.setLayout(enemiesPlayingFieldLayout)

		# buttons
		placeShipBtn = QPushButton("Place Ship")
		placeShipBtn.clicked.connect(self.__startPlaceShip)

		lobbyBtn = QPushButton("Lobby")
		lobbyBtn.clicked.connect(self.__openLobby)

		# status line
		self.__statusLbl = QLabel()
		self.__statusLbl.setStyleSheet("color: #b00")
		self.__updateClientStatus()

		"""
		  column------->
		r
		o
		w
		|
		|
		V

													row		column	height 	width
		"""
		layout = QGridLayout()
		layout.addWidget(self.__statusLbl,            0,        0,     5,      80)
		layout.addWidget(ownPlayingFieldBox,         10,        0,    48,      38)
		layout.addWidget(enemeysPlayingFieldBox,     10,       41,    48,      48)
		layout.addWidget(placeShipBtn,              100,        1,     1,       1)
		layout.addWidget(lobbyBtn,                  100,        0,     1,       1)

		self.setLayout(layout)
		self.setWindowTitle("Battleship++")
		self.resize(1100, 600)
		self.show()

	def __init__(self, backend, fieldLength):
		self.__backend = backend
		self.__viewModel = ViewModel()
		self.__fieldLength = fieldLength

		super(MainForm, self).__init__()
		self.__setupGui()
