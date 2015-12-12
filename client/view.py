from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from playingfield import *

class PlayingFieldWidget(QWidget):
	"""
	Shows a playing field.
	"""

	def _setupGui(self):
		self.resize(400, 400)

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

	def _mapClickToField(self, x, y):
		return (chr(64+y) + str(x))

	def __init__(self, backend):
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

		x, y  = mouseEvent.x() // self._fieldSize, mouseEvent.y() // self._fieldSize
		field = self._mapClickToField(x, y)
		print("Click event at own field: %s | %s" % (field, self._getField(field).status))

	def __init__(self, backend):
		PlayingFieldWidget.__init__(self, backend)

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

		x, y  = mouseEvent.x() // self._fieldSize, mouseEvent.y() // self._fieldSize
		field = self._mapClickToField(x, y)
		print("Click event at enemey's field: %s | %s" % (field, self._getField(field).status))

	def __init__(self, backend):
		PlayingFieldWidget.__init__(self, backend)

class MainForm(QWidget):
	"""
	The main form that shows the complete user interface.
	"""

	def __setupGui(self):
		ownPlayingFieldLbl = QLabel("Your own playing field")
		ownPlayingFieldWgt = OwnPlayingFieldWidget(self.__backend)

		enemeysPlayingFieldLbl = QLabel("Your enemey's playing field")
		enemeysPlayingFieldWgt = EnemeysPlayingFieldWidget(self.__backend)

		layout = QGridLayout()
		layout.addWidget(ownPlayingFieldLbl, 0, 0)
		layout.addWidget(ownPlayingFieldWgt, 1, 0, 12, 6)
		layout.addWidget(enemeysPlayingFieldLbl, 0, 9)
		layout.addWidget(enemeysPlayingFieldWgt, 1, 9, 12, 6)

		self.setLayout(layout)
		self.setWindowTitle("Battleship++")
		self.resize(950, 550)
		self.show()

	def __init__(self, backend):
		self.__backend = backend

		super(MainForm, self).__init__()
		self.__setupGui()
