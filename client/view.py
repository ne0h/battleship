from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from playingfield import *

class ViewModel:

	def __init__(self):
		self.waitForShipPlacement = False
		self.newShipBow = None


class PlayingFieldWidget(QWidget):
	"""
	Shows a playing field.
	"""

	def _setupGui(self):
		self.setMaximumWidth(self._fieldSize*17+1)
		self.setMaximumHeight(self._fieldSize*17+1)

	def paintEvent(self, event):
		"""
		Paints the playing field when an event occurs.

		Args:
			event -- information about the event that occored
		"""

		painter = QPainter()
		painter.begin(self)
		self._drawPlayingField(painter)
		painter.end()

	def _drawPlayingField(self, painter):
		playingField = self._backend.getOwnPlayingField()

		# draw each field
		for i in range(1, len(playingField) + 1):
			for j in range(1, len(playingField) + 1):
				if playingField[i-1][j-1].status is FieldStatus.SHIP:
					painter.setBrush(QColor(210, 105, 30))
				elif playingField[i-1][j-1].status is FieldStatus.SHIPDAMAGED:
					painter.setBrush(QColor(139, 35, 35))
				else:
					painter.setBrush(QColor(0, 191, 255))
				painter.drawRect(i*self._fieldSize, j*self._fieldSize, self._fieldSize, self._fieldSize)

		# draw horizontal and vertical enumeration
		painter.setPen(QColor(0, 0, 0))

		for i in range(1, len(playingField) + 1):
			box = QRectF(i*self._fieldSize, 0, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, str(i))

		for i in range(1, len(playingField) + 1):
			box = QRectF(0, i*self._fieldSize, self._fieldSize, self._fieldSize)
			painter.drawText(box, Qt.AlignCenter, chr(64+i))

	def _mapClickToField(self, mouseEvent):
		x, y  = mouseEvent.x() // self._fieldSize, mouseEvent.y() // self._fieldSize		
		return FieldAddress(x - 1, y - 1)

	def __init__(self, backend, viewModel):
		self._viewModel = viewModel
		self._backend = backend
		self._fieldSize = 25

		super(PlayingFieldWidget, self).__init__()
		self._setupGui()

class OwnPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the user.
	"""

	def _getField(self, field):
		return self._backend.getOwnField(field)

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent -- information about the mouse event
		"""

		fieldAddress = self._mapClickToField(mouseEvent)
		print("Click event at own field: %s | %s" % (fieldAddress.toString(), self._getField(fieldAddress).status))

		if self._viewModel.waitForShipPlacement:
			if self._viewModel.newShipBow is None:
				self._viewModel.newShipBow = fieldAddress
			else:
				ship = self._backend.placeShip(self._viewModel.newShipBow, fieldAddress)

				self.repaint()
				self._viewModel.waitForShipPlacement = False
				self._viewModel.newShipBow = None

	def __init__(self, backend, viewModel):
		PlayingFieldWidget.__init__(self, backend, viewModel)

class EnemeysPlayingFieldWidget(PlayingFieldWidget):
	"""
	Shows the playing field of the enemey.
	"""

	def _getField(self, field):
		return self._backend.getEnemeysField(field)

	def mousePressEvent(self, mouseEvent):
		"""
		This method is called when a mouse event occurs.

		Args:
			mouseEvent -- information about the mouse event
		"""

		field = self._mapClickToField(mouseEvent)
		print("Click event at enemey's field: %s | %s" % (field, self._getField(field).status))

	def __init__(self, backend, viewModel):
		PlayingFieldWidget.__init__(self, backend, viewModel)

class MainForm(QWidget):
	"""
	The main form that shows the complete user interface.
	"""

	def __startPlaceShip(self):
		self.__viewModel.waitForShipPlacement = True

	def __setupGui(self):
		placeShipBtn = QPushButton("Place Ship")
		placeShipBtn.clicked.connect(self.__startPlaceShip)

		ownPlayingFieldLbl = QLabel("Your own playing field")
		ownPlayingFieldWgt = OwnPlayingFieldWidget(self.__backend, self.__viewModel)

		enemeysPlayingFieldLbl = QLabel("Your enemey's playing field")
		enemeysPlayingFieldWgt = EnemeysPlayingFieldWidget(self.__backend, self.__viewModel)

		layout = QGridLayout()
		layout.addWidget(placeShipBtn, 14, 0)
		layout.addWidget(ownPlayingFieldLbl, 1, 0)
		layout.addWidget(ownPlayingFieldWgt, 2, 0, 12, 6)
		layout.addWidget(enemeysPlayingFieldLbl, 1, 9)
		layout.addWidget(enemeysPlayingFieldWgt, 2, 9, 12, 6)

		self.setLayout(layout)
		self.setWindowTitle("Battleship++")
		self.resize(950, 550)
		self.show()

	def __init__(self, backend):
		self.__backend = backend
		self.__viewModel = ViewModel()

		super(MainForm, self).__init__()
		self.__setupGui()
