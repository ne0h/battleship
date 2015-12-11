from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from playingfield import *

class PlayingFieldWidget(QWidget):

	def __setupGui(self):
		self.resize(400, 400)

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.__drawPlayingField(painter)
		painter.end()

	def __drawPlayingField(self, painter):
		playingField = self.__backend.getOwnPlayingField()

		# draw each field
		for i in range(1, len(playingField) + 1):
			for j in range(1, len(playingField) + 1):
				if playingField[i-1][j-1].status is FieldStatus.SHIP:
					painter.setBrush(QColor(210, 105, 30))
				elif playingField[i-1][j-1].status is FieldStatus.SHIPDAMAGED:
					painter.setBrush(QColor(139, 35, 35))
				else:
					painter.setBrush(QColor(0, 191, 255))
				painter.drawRect(i*self.__fieldSize, j*self.__fieldSize, self.__fieldSize, self.__fieldSize)

		# draw horizontal and vertical enumeration
		painter.setPen(QColor(0, 0, 0))

		for i in range(1, len(playingField) + 1):
			box = QRectF(i*self.__fieldSize, 0, self.__fieldSize, self.__fieldSize)
			painter.drawText(box, Qt.AlignCenter, str(i))

		for i in range(1, len(playingField) + 1):
			box = QRectF(0, i*self.__fieldSize, self.__fieldSize, self.__fieldSize)
			painter.drawText(box, Qt.AlignCenter, chr(64+i))

	def __mapClickToField(self, x, y):
		return (chr(64+y) + str(x))

	def mousePressEvent(self, mouseEvent):
		x, y  = mouseEvent.x() // self.__fieldSize, mouseEvent.y() // self.__fieldSize
		field = self.__mapClickToField(x, y)
		print("Click event at: %s | %s" % (field, self.__backend.getOwnField(field).status))

	def __init__(self, backend):
		self.__backend = backend
		self.__fieldSize = 25

		super(PlayingFieldWidget, self).__init__()
		self.__setupGui()

class MainForm(QWidget):

	def __setupGui(self):
		headLbl = QLabel("Welcome to Battleship++!")
		playingFieldWgt = PlayingFieldWidget(self.__backend)

		layout = QGridLayout()
		layout.addWidget(headLbl, 0, 0)
		layout.addWidget(playingFieldWgt, 1, 0, 6, 3)

		self.setLayout(layout)
		self.setWindowTitle("Battleship++")
		self.resize(550, 550)
		self.show()

	def __init__(self, backend):
		self.__backend = backend

		super(MainForm, self).__init__()
		self.__setupGui()
