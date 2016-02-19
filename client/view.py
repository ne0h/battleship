import abc, logging
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from playingfield import *

class ViewModel:

	def __init__(self):
		self.waitForShipPlacement = False
		self.waitForAttack = False
		self.waitForSpecialAttack = False

		self.waitForMoveNorth = False
		self.waitForMoveWest  = False
		self.waitForMoveSouth = False
		self.waitForMoveEast  = False

		self.newShipBow = None

class ConnectDialog(QDialog):

	def __showSettingsErrorBox(self, title="Connection settings wrong.", text="Enter valid connection settings."):
		QMessageBox.about(self, title, text)

	def __connect(self):
		try:
			nickname = self.__nicknameIpt.text()
			hostname = self.__hostnameIpt.text()
			port     = int(self.__portIpt.text())
		except ValueError:
			logging.error("Port is not a number.")
			self.__showSettingsErrorBox()

		if not hostname:
			self.__showSettingsErrorBox()
		else:
			if self.__backend.connect(nickname, hostname, port):
				self.close()
			else:
				self.__showSettingsErrorBox(text="Server not reachable.")

	def __updateServerAddress(self):
		self.__hostnameIpt.setText(self.__serversWgt.currentItem().text())
		self.__portIpt.setText("12345")

	def __onUpdateServers(self, servers):
		for server in servers:
			found = False
			for i in range(0, self.__serversWgt.count()):
				if self.__serversWgt.item(i).text():
					found = True
					break
			if not found:
				self.__serversWgt.addItem(server)

	def __setupGui(self):
		self.__serversWgt = QListWidget()
		self.__serversWgt.setSortingEnabled(True)
		self.__serversWgt.clicked.connect(self.__updateServerAddress)

		self.__nicknameIpt = QLineEdit()
		self.__nicknameIpt.setFixedWidth(100)
		self.__nicknameIpt.setFixedHeight(20)
		self.__nicknameIpt.setPlaceholderText("Nickname")

		self.__hostnameIpt = QLineEdit()
		self.__hostnameIpt.setFixedWidth(150)
		self.__hostnameIpt.setFixedHeight(20)
		self.__hostnameIpt.setText("localhost")
		self.__hostnameIpt.setPlaceholderText("Hostname")

		self.__portIpt = QLineEdit()
		self.__portIpt.setFixedWidth(60)
		self.__portIpt.setFixedHeight(20)
		self.__portIpt.setText("44444")
		self.__portIpt.setPlaceholderText("Port")

		self.__returnBtn = QPushButton("Connect")
		self.__returnBtn.clicked.connect(self.__connect)

		bottomLayout = QHBoxLayout()
		bottomLayout.addWidget(self.__nicknameIpt)
		bottomLayout.addWidget(self.__hostnameIpt)
		bottomLayout.addWidget(self.__portIpt)
		bottomLayout.addWidget(self.__returnBtn)
		bottomLbl = QLabel()
		bottomLbl.setMinimumHeight(40)
		bottomLbl.setLayout(bottomLayout)

		layout = QVBoxLayout()
		layout.addWidget(self.__serversWgt)
		layout.addWidget(bottomLbl)

		self.setLayout(layout)
		self.setWindowTitle("Find a server")
		self.resize(500, 300)

	def __init__(self, backend):
		from backend import Callback

		super(ConnectDialog, self).__init__()
		self.__backend = backend
		self.__setupGui()

		cb = Callback()
		cb.onAction = lambda servers: self.__onUpdateServers(servers)
		self.__onUpdateServers(self.__backend.registerUdpDiscoveryCallback(cb))

class LobbyDialog(QDialog):

	def __interfaceEnabled(self, value):
		self.__gamesWidget.setEnabled(value)
		self.__joinGameBtn.setEnabled(value)
		self.__createGameIpt.setEnabled(value)
		self.__createGameBtn.setEnabled(value)

	def __joinGameOnClick(self):
		from backend import Callback

		gameId = self.__gamesWidget.currentItem().text().split(":")[0]
		cb = Callback()
		cb.onAction = lambda success: self.__onJoinGame(success)
		self.__backend.joinGame(gameId, cb)
		self.__interfaceEnabled(False)

	def __onJoinGame(self, success):
		logging.info("Game joined? " + str(success))
		if success:
			self.close()
		else:
			self.__error("Failed to join game. Please choose another one.")
			self.__interfaceEnabled(True)

	def __createGameOnClick(self):
		from backend import Callback

		# TODO validate ipt length
		gameId = self.__createGameIpt.text()
		logging.info("Creating game: %s", gameId)
		cb = Callback()
		cb.onAction = lambda success: self.__onCreateGame(success)
		self.__backend.createGame(gameId, cb)
		self.__interfaceEnabled(False)

	def __onCreateGame(self, success):
		logging.info("Creation of game successful: %s", (success))
		if success:
			self.close()
		else:
			self.__error("Failed create join game.")
			self.__interfaceEnabled(True)

	def __error(self, message):
		self.__errorBox.setText(message)

	def __setupGui(self):
		self.__statusLbl = QLabel()
		self.__gamesWidget = QListWidget()
		self.__gamesWidget.setSortingEnabled(True)
		self.__errorBox = QLabel()
		self.__errorBox.setStyleSheet("color: #b00")
		self.__joinGameBtn = QPushButton("Join game")
		self.__joinGameBtn.clicked.connect(self.__joinGameOnClick)

		self.__createGameIpt = QLineEdit()
		self.__createGameBtn = QPushButton("Create game")
		self.__createGameBtn.clicked.connect(self.__createGameOnClick)

		btnsLayout = QHBoxLayout()
		btnsLayout.addWidget(self.__createGameIpt)
		btnsLayout.addWidget(self.__createGameBtn)
		btnsWgt = QWidget()
		btnsWgt.setLayout(btnsLayout)

		layout = QVBoxLayout()
		layout.addWidget(self.__statusLbl)
		layout.addWidget(self.__gamesWidget)
		layout.addWidget(self.__errorBox)
		layout.addWidget(self.__joinGameBtn)
		layout.addWidget(btnsWgt)

		self.setLayout(layout)
		self.setWindowTitle("Lobby")
		self.resize(600, 500)
		self.show()

	def __onUpdateGamesList(self):
		self.__statusLbl.setText("%s players currently online and %s games are open!"
								 % (len(self.__backend.lobby.players), len(self.__backend.lobby.games)))

		# only add new games
		for game in self.__backend.lobby.games:
			found = -1
			for i in range(0, self.__gamesWidget.count()):
				# this validation is sufficient, because colons are not allowed as values in the protocol
				if self.__gamesWidget.item(i).text().startswith("%s:" % (game.name)):
					found = i
					break

			text = "%s: %s" % (game.name, self.__backend.lobby.getNickname(game.players[0]))
			if len(game.players) is 1:
				text = "%s is waiting for an oppenent" % text
			else:
				text = "%s vs. %s" % (text, game.players[1])

			# is there an update? if yes - update corresponding item
			# if not - add the new item
			if found is not -1:
				self.__gamesWidget.item(i).text = text
			else:
				self.__gamesWidget.addItem(text)

	def closeEvent(self, event):
		#self.__backend.removeLobbyUpdateGamesCallback(self.__gamesListCb)
		pass

	def __init__(self, backend):
		from backend import Callback

		self.__backend = backend
		self.__gamesListCb = Callback()
		self.__gamesListCb.onAction = lambda: self.__onUpdateGamesList()
		players, games = self.__backend.registerLobbyUpdateGamesCallback(self.__gamesListCb)

		super(LobbyDialog, self).__init__()
		self.__setupGui()
		self.__onUpdateGamesList()

class PlayingFieldWidget(QWidget):
	"""
	Shows a playing field.
	"""

	def _setupGui(self):
		self.setMaximumWidth(self._fieldSize  * 18 + 1)
		self.setMaximumHeight(self._fieldSize * 18 + 1)

	@abc.abstractmethod
	def _getShips(self):
		pass

	def paintEvent(self, event):
		"""
		Paints the playing field when an event occurs.

		Args:
			event: information about the event that occured
		"""

		painter = QPainter()
		painter.begin(self)
		self._drawPlayingField(painter)
		painter.end()

	def _drawPlayingField(self, painter):

		# fill each field with water
		for i in range(1, self._fieldLength + 1):
			for j in range(1, self._fieldLength + 1):
				if self._backend.isUnfogged(Field(i - 1, j - 1)):
					painter.setBrush(QColor(0, 191, 255))
				else:
					painter.setBrush(QColor(230, 230, 230))
				painter.drawRect(i * self._fieldSize, j * self._fieldSize, self._fieldSize, self._fieldSize)

		# add ships
		painter.setBrush(QColor(210, 105, 30))
		for ship in self._getShips():
			import os
			dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))

			# draw bow
			bow = ship.bow
			if ship.isDamaged(bow):
				pass
			else:
				painter.drawPixmap((bow.x + 1) * self._fieldSize, (16 - bow.y) * self._fieldSize, self._fieldSize,
									self._fieldSize, QPixmap(dir + "/img/bow_" + ship.orientation.value + ".png"))

			# draw rear
			rear = ship.rear
			if ship.isDamaged(rear):
				pass
			else:
				painter.drawPixmap((rear.x + 1) * self._fieldSize, (16 - rear.y) * self._fieldSize, self._fieldSize,
									self._fieldSize, QPixmap(dir + "/img/rear_" + ship.orientation.value + ".png"))

			# draw the rest
			for middle in ship.middles:
				if ship.isDamaged(middle):
					pass
				else:
					painter.drawPixmap((middle.x + 1) * self._fieldSize, (16 - middle.y) * self._fieldSize,
										self._fieldSize, self._fieldSize,
										QPixmap(dir + "/img/middle_" + ship.orientation.value + ".png"))

		# draw horizontal and vertical enumeration
		painter.setPen(QColor(0, 0, 0))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(i*self._fieldSize, 0, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, chr(64 + i))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(i*self._fieldSize, 17*self._fieldSize, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, chr(64 + i))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(0, (17-i)*self._fieldSize, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, str(i))

		for i in range(1, self._fieldLength + 1):
			box = QRectF(17*self._fieldSize, (17-i)*self._fieldSize, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, str(i))

	def _mapClickToField(self, mouseEvent):
		x, y  = mouseEvent.x() // self._fieldSize, mouseEvent.y() // self._fieldSize
		return Field(x - 1, 16 - y)

	def __init__(self, backend, viewModel, fieldLength, devmode, fieldSize=25):
		self._viewModel = viewModel
		self._backend = backend
		self._fieldSize = fieldSize
		self._fieldLength = fieldLength
		self._devmode = devmode

		super(PlayingFieldWidget, self).__init__()
		self.setMinimumWidth(450)
		self._setupGui()

class OwnPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the user.
	"""

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent: information about the mouse event
		"""

		fieldAddress = self._mapClickToField(mouseEvent)
		logging.debug("Click event at own field: %s" % (fieldAddress.toString()))

		if self._viewModel.waitForShipPlacement:
			if self._viewModel.newShipBow is None:
				self._viewModel.newShipBow = fieldAddress
			else:
				moreShips = self._backend.placeShip(fieldAddress, self._viewModel.newShipBow)
				self.repaint()

				if not moreShips:
					self._viewModel.waitForShipPlacement = True
				self._viewModel.newShipBow = None

		#
		# Moves
		#
		if self._viewModel.waitForMoveNorth:
			# get shipId
			shipId = self._backend.getShipAtPosition(field)
			if shipId > 0:
				logging.info("Moving ship #%s to the north" % str(shipId))
				self._backend.move(shipId, Orientation.NORTH)

		if self._viewModel.waitForMoveWest:
			# get shipId
			shipId = self._backend.getShipAtPosition(field)
			if shipId > 0:
				logging.info("Moving ship #%s to the west" % str(shipId))
				self._backend.move(shipId, Orientation.WEST)

		if self._viewModel.waitForMoveSouth:
			# get shipId
			shipId = self._backend.getShipAtPosition(field)
			if shipId > 0:
				logging.info("Moving ship #%s to the south" % str(shipId))
				self._backend.move(shipId, Orientation.SOUTH)

		if self._viewModel.waitForMoveEast:
			# get shipId
			shipId = self._backend.getShipAtPosition(field)
			if shipId > 0:
				logging.info("Moving ship #%s to the east" % str(shipId))
				self._backend.move(shipId, Orientation.EAST)

		if self._devmode:
			self.repaint()

	def _getShips(self):
		return self._backend.getOwnShips()

	def __init__(self, backend, viewModel, fieldLength, devmode):
		PlayingFieldWidget.__init__(self, backend, viewModel, fieldLength, devmode)

class EnemeysPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the enemey.
	"""

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent: information about the mouse event
		"""

		field = self._mapClickToField(mouseEvent)

		#
		# Attacks
		#
		if self._viewModel.waitForAttack:
			logging.info("Attack at enemey's field: %s" % (field.toString()))
			self._backend.attack(field)
			self._viewModel.waitForAttack = False

		if self._viewModel.waitForSpecialAttack:
			logging.info("Special Attack at enemey's field: %s" % (field.toString()))
			self._backend.specialAttack(field)
			self._viewModel.waitForSpecialAttack = False

		if self._devmode:
			self.repaint()

	def _getShips(self):
		return self._backend.getEnemeysShips()

	def __init__(self, backend, viewModel, fieldLength, devmode):
		PlayingFieldWidget.__init__(self, backend, viewModel, fieldLength, devmode)

class MainForm(QWidget):
	"""
	The main form that shows the complete user interface.
	"""

	def __showMessageBox(self, title, text):
		QMessageBox.about(self, title, text)

	def __startPlaceShip(self):
		self.__viewModel.waitForShipPlacement = True

	def __setGamePlayButtons(self, value):
		self.__attackBtn.setEnabled(value)
		self.__specialAttackBtn.setEnabled(value)
		self.__moveNorthBtn.setEnabled(value)
		self.__moveWestBtn.setEnabled(value)
		self.__moveSouthBtn.setEnabled(value)
		self.__moveEastBtn.setEnabled(value)

	def __enableGamePlayButtons(self):
		self.__setGameButtons(True)

	def __disableGamePlayButtons(self):
		self.__setGamePlayButtons(False)

	def __openLobby(self):
		import sys
		from backend import ClientStatus

		if not self.__lobbyAlreadyOpen:
			self.__lobbyAlreadyOpen = True
			LobbyDialog(self.__backend).exec_()
			self.__lobbyAlreadyOpen = False

			# lobby closed, check current client status
			if self.__backend.clientStatus is ClientStatus.PREPARATIONS:
				self.__placeShipBtn.setEnabled(True)
				self.__lobbyBtn.setEnabled(False)

	def __onUpdateShipList(self, shipId):

		# validate if the ship is already in the list
		found = False
		for i in range(0, self.__shipsWgt.count()):
			if self.__shipsWgt.item(i).text().startswith("#%s:" % shipId):
				found = True
				break
		if not found:
			ship = self.__backend.getOwnShip(shipId)
			self.__shipsWgt.addItem("#%s: %s:%s" % (shipId, ship.bow.toString(), ship.rear.toString()))

	def __onUpdateClientStatus(self):
		from backend import ClientStatus

		status = self.__backend.clientStatus
		if status is ClientStatus.NOTCONNECTED:
			self.__statusLbl.setText("Please connect to a server.")
		elif status is ClientStatus.NOGAMERUNNING:
			self.__statusLbl.setText("No game running, please use the lobby to connect to a game.")
			self.__lobbyBtn.setEnabled(True)
			self.__connectBtn.setEnabled(False)
		elif status is ClientStatus.PREPARATIONS:
			from backend import Callback

			self.__statusLbl.setText("Please place your ships.")
			self.__leaveGameBtn.setEnabled(True)
			self.__updatePlayersLbl()

			cb = Callback()
			cb.onAction = lambda shipId: self.__onUpdateShipList(shipId)
			self.__backend.registerShipUpdateCallback(cb)
		elif status is ClientStatus.WAITINGFOROPPONENT:
			self.__statusLbl.setText("Placement of ships successful. Waiting for opponent now.")
			self.__placeShipBtn.setEnabled(False)
			self.__connectBtn.setEnabled(False)
			self.__lobbyBtn.setEnabled(False)
		elif status is ClientStatus.OWNTURN:
			self.__status.setText("It is your turn.")
			self.__enableGamePlayButtons()
		elif status is ClientStatus.OPPONENTSTURN:
			self.__statusLbl.setText("Please wait for your opponent.")
			self.__disableGamePlayButtons()
		elif status is ClientStatus.YOUWIN:
			self.__statusLbl.setText("You win!")
			self.__disableGamePlayButtons()
			# TODO: reset client
		elif status is ClientStatus.YOULOSE:
			self.__statusLbl.setText("You lose!")
			self.__disableGamePlayButtons()
			# TODO: reset client

	def __leaveGameCalled(self):
		logging.info("Game aborted. Preparing client for a new game.")
		self.__showMessageBox("Game aborted", "Game aborted. You can now join or create another one.")
		self.__resetClient()

	def __leaveGame(self):
		from backend import Callback

		cb = Callback()
		cb.onAction = lambda: self.__leaveGameCalled()
		self.__backend.leaveGame(cb)

	def __resetClient(self):
		self.__lobbyBtn.setEnabled(True)
		self.__placeShipBtn.setEnabled(False)
		self.__leaveGameBtn.setEnabled(False)

	def __connectCalled(self):
		pass

	def __openConnectDialog(self):
		import sys

		if not self.__connectDialogAlreadyOpen:
			self.__connectDialogAlreadyOpen = True
			ConnectDialog(self.__backend).exec_()
			self.__connectDialogAlreadyOpen = False

		"""
		from backend import Callback

		cb = Callback()
		cb.onAction = lambda success: self.__connectCalled(success)
		#self.__backend.connect()
		"""

	def __attackResponse(self, success, result):
		pass

	def __attack(self):
		self.__waitForAttack = True

	def __specialAttack(self):
		pass

	def __moveShip(self):
		pass

	def __onJoinGame(self):
		self.__updateStatusLbl()

	def __updatePlayersLbl(self):
		nickname = self.__backend.lobby.getOwnNickname()
		if self.__backend.lobby.hasGame():
			if self.__backend.lobby.hasOpponent():
				opponent = self.__backend.lobby.getNickname(self.__backend.lobby.opponent)
				self.__playersLbl.setText("Current game: %s vs. %s" % (nickname, opponent))
			else:
				self.__playersLbl.setText("Current game: %s vs." % nickname)

	def __sendChatMessage(self):
		# TODO: Check for empty strings
		msg = self.__chatIpt.text()
		self.__backend.sendChatMessage(msg)
		self.__chatIpt.setText("")

	def __onIncomingChatMessage(self, authorId, timestamp, message):
		self.__chatLog.append("(%s) %s: %s" % (timestamp, authorId, message))

	def __onError(self, error):
		self.__statusLbl.setText("Error: %s" % error)

	def __moveNorth(self):
		self.__viewModel.waitForMoveNorth = True

	def __moveWest(self):
		self.__viewModel.waitForMoveWest = True

	def __moveSouth(self):
		self.__viewModel.waitForMoveSouth = True

	def __moveEast(self):
		self.__viewModel.waitForEast = True

	def __setupGui(self, nickname, devmode):

		#
		# own playing field stuff
		#
		ownPlayingFieldBox = QGroupBox("Your own playing field")
		ownPlayingFieldWgt = OwnPlayingFieldWidget(self.__backend, self.__viewModel, self.__fieldLength, devmode)
		ownPlayingFieldLayout = QVBoxLayout()
		ownPlayingFieldLayout.addWidget(ownPlayingFieldWgt)
		ownPlayingFieldBox.setLayout(ownPlayingFieldLayout)

		#
		# enemies playing field stuff
		#
		enemeysPlayingFieldBox = QGroupBox("Your enemey's playing field")
		enemeysPlayingFieldWgt = EnemeysPlayingFieldWidget(self.__backend, self.__viewModel, self.__fieldLength, devmode)
		enemiesPlayingFieldLayout = QVBoxLayout()
		enemiesPlayingFieldLayout.addWidget(enemeysPlayingFieldWgt)
		enemeysPlayingFieldBox.setLayout(enemiesPlayingFieldLayout)

		#
		# shiplist with game play buttons
		#
		shipsBox = QGroupBox("Your ships")
		self.__shipsWgt = QListWidget()
		self.__shipsWgt.setMaximumWidth(200)
		self.__shipsWgt.setSortingEnabled(True)
		self.__attackBtn = QPushButton("Attack")
		self.__attackBtn.clicked.connect(self.__attack)
		self.__specialAttackBtn = QPushButton("Special Attack")
		self.__specialAttackBtn.clicked.connect(self.__specialAttack)

		self.__moveNorthBtn = QPushButton("N")
		self.__moveNorthBtn.clicked.connect(self.__moveNorth)
		self.__moveWestBtn  = QPushButton("W")
		self.__moveWestBtn.clicked.connect(self.__moveWest)
		self.__moveSouthBtn = QPushButton("S")
		self.__moveSouthBtn.clicked.connect(self.__moveSouth)
		self.__moveEastBtn  = QPushButton("E")
		self.__moveEastBtn.clicked.connect(self.__moveEast)
		moveLayout = QHBoxLayout()
		moveLayout.addWidget(self.__moveNorthBtn)
		moveLayout.addWidget(self.__moveWestBtn)
		moveLayout.addWidget(self.__moveSouthBtn)
		moveLayout.addWidget(self.__moveEastBtn)
		moveWgt = QWidget()
		moveWgt.setLayout(moveLayout)
		self.__disableGamePlayButtons()

		shipsLayout = QVBoxLayout()
		shipsLayout.addWidget(self.__shipsWgt)
		shipsLayout.addWidget(self.__attackBtn)
		shipsLayout.addWidget(self.__specialAttackBtn)
		shipsLayout.addWidget(moveWgt)
		shipsBox.setLayout(shipsLayout)

		# buttons
		self.__placeShipBtn = QPushButton("Place Ships")
		self.__placeShipBtn.clicked.connect(self.__startPlaceShip)
		self.__placeShipBtn.setEnabled(False)

		self.__lobbyBtn = QPushButton("Lobby")
		self.__lobbyBtn.clicked.connect(self.__openLobby)
		self.__lobbyBtn.setEnabled(False)

		self.__leaveGameBtn = QPushButton("Leave Game")
		self.__leaveGameBtn.clicked.connect(self.__leaveGame)
		self.__leaveGameBtn.setEnabled(False)

		self.__connectBtn = QPushButton("Connect")
		self.__connectBtn.clicked.connect(self.__openConnectDialog)

		# status stuff
		self.__statusLbl = QLabel()
		self.__statusLbl.setStyleSheet("color: #b00")
		self.__statusLbl.setMinimumWidth(800)
		# TODO: align right side

		self.__playersLbl = QLabel()
		self.__playersLbl.setStyleSheet("color: #00b")
		if nickname:
			self.__playersLbl.setText("Nickname: %s" % nickname)
		else:
			self.__playersLbl.setText("Nickname: Unnamed Player")

		topLayout = QHBoxLayout()
		topLayout.addWidget(self.__statusLbl)
		topLayout.addWidget(self.__playersLbl)
		topWgt = QWidget()
		topWgt.setLayout(topLayout)

		# chat stuff
		self.__chatLog = QTextEdit()
		self.__chatLog.setReadOnly(True)
		self.__chatLog.setMinimumHeight(150)
		self.__chatLog.ensureCursorVisible()
		self.__chatIpt = QLineEdit()
		self.__chatIpt.setPlaceholderText("Message")
		chatBtn = QPushButton("Send")
		chatBtn.clicked.connect(self.__sendChatMessage)

		chatLayout = QHBoxLayout()
		chatLayout.addWidget(self.__chatIpt)
		chatLayout.addWidget(chatBtn)
		chatWgt = QWidget()
		chatWgt.setLayout(chatLayout)

		#
		# place all elements
		#
		playingFieldLayout = QHBoxLayout()
		playingFieldLayout.addWidget(ownPlayingFieldBox)
		playingFieldLayout.addWidget(shipsBox)
		playingFieldLayout.addWidget(enemeysPlayingFieldBox)
		playingFieldWgt = QWidget()
		playingFieldWgt.setLayout(playingFieldLayout)
		playingFieldWgt.setMinimumWidth(1300)
		playingFieldWgt.setMinimumHeight(510)

		btnsLayout = QHBoxLayout()
		btnsLayout.addWidget(self.__connectBtn)
		btnsLayout.addWidget(self.__lobbyBtn)
		btnsLayout.addWidget(self.__placeShipBtn)
		btnsLayout.addWidget(self.__leaveGameBtn)
		btnsWgt = QWidget()
		btnsWgt.setLayout(btnsLayout)

		layout = QVBoxLayout()
		layout.addWidget(topWgt)
		layout.addWidget(playingFieldWgt)
		layout.addWidget(btnsWgt)
		layout.addWidget(self.__chatLog)
		layout.addWidget(chatWgt)

		self.setLayout(layout)
		self.setWindowTitle("Battleship++")
		self.show()

	def closeEvent(self, event):
		self.__backend.close()

	def __init__(self, backend, fieldLength, devmode, nickname=None):
		from backend import Callback

		self.__backend = backend
		self.__viewModel = ViewModel()
		self.__fieldLength = fieldLength
		self.__connectDialogAlreadyOpen = False
		self.__lobbyAlreadyOpen = False

		super(MainForm, self).__init__()
		self.__setupGui(nickname, devmode)

		clientStatusCb = Callback()
		clientStatusCb.onAction = lambda: self.__onUpdateClientStatus()
		self.__backend.registerClientStatusCallback(clientStatusCb)
		self.__onUpdateClientStatus()

		chatCb = Callback()
		chatCb.onAction = lambda authorId, timestamp, message: self.__onIncomingChatMessage(authorId, timestamp,
																							message)
		self.__backend.registerChatCallback(chatCb)

		errorCb = Callback()
		errorCb.onAction = lambda error: self.__onError(error)
		self.__backend.registerErrorCallback(errorCb)

		opponentJoinedCb = Callback()
		opponentJoinedCb.onAction = lambda: self.__updatePlayersLbl()
		self.__backend.registerOpponentJoinedGameCallback(opponentJoinedCb)
