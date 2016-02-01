import sys
sys.path.append("..")

import unittest
from playingfield import *

class TestShipList(unittest.TestCase):

	FIELDLENGTH = 16

	def test_borderCollisionWhilePlacingShip(self):
		ships = ShipList(self.FIELDLENGTH)

		ships.add(Field(-1,  3), Field(2 ,  3))
		ships.add(Field(14,  3), Field(16,  3))

		ships.add(Field( 3, -1), Field(3 ,  2))
		ships.add(Field( 3, 16), Field(3 , 13))

		ships.add(Field( 2,  3), Field(-1,  3))
		ships.add(Field(16,  3), Field(14,  3))

		ships.add(Field( 3,  2), Field(3 , -1))
		ships.add(Field( 3, 13), Field(3 , 16))

		self.assertEqual(ships.getShipCount(), 0)

	def test_collidingShips(self):
		ships = ShipList(self.FIELDLENGTH)
		ships.add(Field(3, 4), Field(6, 4))

		ships.add(Field(6, 4), Field(8, 4))
		ships.add(Field(1, 4), Field(3, 4))
		ships.add(Field(3, 2), Field(3, 4))

		self.assertEqual(ships.getShipCount(), 1)

	def test_addToManyCarriers(self):
		ships = ShipList(self.FIELDLENGTH)

		ships.add(Field(0, 0), Field(0, 4))
		self.assertEqual(ships.getCarrierCount(), 1)

		ships.add(Field(0, 0), Field(0, 4))
		self.assertEqual(ships.getCarrierCount(), 1)

	def test_addToManyBattleships(self):
		ships = ShipList(self.FIELDLENGTH)

		ships.add(Field(0, 0), Field(0, 3))
		ships.add(Field(1, 0), Field(1, 3))
		self.assertEqual(ships.getBattleshipCount(), 2)

		ships.add(Field(1, 0), Field(1, 3))
		self.assertEqual(ships.getBattleshipCount(), 2)

	def test_addToManyCruisers(self):
		ships = ShipList(self.FIELDLENGTH)

		ships.add(Field(0, 0), Field(0, 2))
		ships.add(Field(1, 0), Field(1, 2))
		ships.add(Field(2, 0), Field(2, 2))
		self.assertEqual(ships.getCruiserCount(), 3)
		
		ships.add(Field(3, 0), Field(3, 2))
		self.assertEqual(ships.getCruiserCount(), 3)

	def test_addToManyDestroyers(self):
		ships = ShipList(self.FIELDLENGTH)

		ships.add(Field(0, 0), Field(0, 1))
		ships.add(Field(1, 0), Field(1, 1))
		ships.add(Field(2, 0), Field(2, 1))
		ships.add(Field(3, 0), Field(3, 1))
		self.assertEqual(ships.getDestroyerCount(), 4)

		ships.add(Field(3, 0), Field(3, 1))
		self.assertEqual(ships.getDestroyerCount(), 4)		

if __name__ == "__main__":
	unittest.main()
