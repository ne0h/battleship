import sys
sys.path.append("..")

import unittest
from playingfield import *

class TestShipList(unittest.TestCase):

	FIELDLENGTH = 16

	def test_borderCollisionWhilePlacingShip(self):
		ships = ShipList(self.FIELDLENGTH)

		self.assertIsNone(ships.add(Field(-1,  3), Field(2 ,  3)))
		self.assertIsNone(ships.add(Field(14,  3), Field(16,  3)))

		self.assertIsNone(ships.add(Field(3 , -1), Field(3 ,  2)))
		self.assertIsNone(ships.add(Field(3 , 16), Field(3 , 13)))

		self.assertIsNone(ships.add(Field(2 ,  3), Field(-1,  3)))
		self.assertIsNone(ships.add(Field(16,  3), Field(14,  3)))

		self.assertIsNone(ships.add(Field(3 ,  2), Field(3 , -1)))
		self.assertIsNone(ships.add(Field(3 , 13), Field(3 , 16)))

	def test_collidingShips(self):
		ships = ShipList(self.FIELDLENGTH)
		ships.add(Field(3, 4), Field(6, 4))

		self.assertIsNone(ships.add(Field(6, 4), Field(8, 4)))
		self.assertIsNone(ships.add(Field(1, 4), Field(3, 4)))
		self.assertIsNone(ships.add(Field(3, 2), Field(3, 4)))

	def test_addToManyBattleships(self):
		ships = ShipList(self.FIELDLENGTH)

		ship1 = ships.add(Field(0, 0), Field(0, 4))
		self.assertIsInstance(ship1, Battleship)

		ship2 = ships.add(Field(1, 0), Field(1, 4))
		self.assertIsNone(ship2)

	def test_addToManyDestroyers(self):
		ships = ShipList(self.FIELDLENGTH)

		ship1 = ships.add(Field(0, 0), Field(0, 3))
		self.assertIsInstance(ship1, Destroyer)

		ship2 = ships.add(Field(1, 0), Field(1, 3))
		self.assertIsInstance(ship2, Destroyer)

		ship3 = ships.add(Field(2, 0), Field(2, 3))
		self.assertIsNone(ship3)

	def test_addToManyCruisers(self):
		ships = ShipList(self.FIELDLENGTH)

		ship1 = ships.add(Field(0, 0), Field(0, 2))
		self.assertIsInstance(ship1, Cruiser)

		ship2 = ships.add(Field(1, 0), Field(1, 2))
		self.assertIsInstance(ship2, Cruiser)

		ship3 = ships.add(Field(2, 0), Field(2, 2))
		self.assertIsInstance(ship3, Cruiser)

		ship4 = ships.add(Field(3, 0), Field(3, 2))
		self.assertIsNone(ship4)

	def test_addToManySubmarines(self):
		ships = ShipList(self.FIELDLENGTH)

		ship1 = ships.add(Field(0, 0), Field(0, 1))
		self.assertIsInstance(ship1, Submarine)

		ship2 = ships.add(Field(1, 0), Field(1, 1))
		self.assertIsInstance(ship2, Submarine)

		ship3 = ships.add(Field(2, 0), Field(2, 1))
		self.assertIsInstance(ship3, Submarine)

		ship4 = ships.add(Field(3, 0), Field(3, 1))
		self.assertIsInstance(ship4, Submarine)

		ship5 = ships.add(Field(4, 0), Field(4, 1))
		self.assertIsNone(ship5)

if __name__ == "__main__":
	unittest.main()
