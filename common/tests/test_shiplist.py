import sys
sys.path.append("..")

import unittest
from playingfield import *

class TestShipList(unittest.TestCase):

	FIELDLENGTH = 16

	def test_borderCollisionWhilePlacingShip(self):
		"""
		Checks that the x und y are in border: 0<=x<=15 AND 0<=y<=15		
		"""		
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
	
	def test_diagonalPlacingShip(self):
		"""
		If the ship is diagonal: not(x1=x2 or y1=y2) the return false		
		"""
		ships = ShipList(self.FIELDLENGTH)  # Invalid: not (x1=x2 or y1=y2)
		ships.add(Field(2,  3), Field(3 ,  4))
		self.assertEqual(ships.getShipCount(), 0)

	def test_addTooLongShip(self):
		"""
		If the ship is too long: ShipLenght>5 then return false		
		"""		
		ships = ShipList(self.FIELDLENGTH)  # Invalid: ShipLenght>5
		ships.add(Field(2,  3), Field(2 ,  8))
		self.assertEqual(ships.getShipCount(), 0)
	
	def test_addTooShortShip(self):
		"""
		If the ship is too short: ShipLenght<2 then return false 		
		"""
		ships = ShipList(self.FIELDLENGTH)  # Invalid: ShipLenght<2
		ships.add(Field(2,  3), Field(2 ,  3))
		self.assertEqual(ships.getShipCount(), 0)

	def test_collidingShips(self):
		"""
		Checks that the ships don't collide with each other		
		"""		
		ships = ShipList(self.FIELDLENGTH)
		ships.add(Field(3, 4), Field(6, 4))  # x1=3,x2=6, y1=y2=4 
		
		#Collision mit x2=6,y2=4
		ships.add(Field(6, 4), Field(8, 4))
		ships.add(Field(4, 4), Field(6, 4))
		ships.add(Field(6, 2), Field(6, 4))
		ships.add(Field(6, 4), Field(6, 8))
		
		#Collision mit x1=3,y1=4
		ships.add(Field(1, 4), Field(3, 4))
		ships.add(Field(3, 4), Field(5, 4))
		ships.add(Field(3, 2), Field(3, 4))
		ships.add(Field(3, 4), Field(3, 6))

		self.assertEqual(ships.getShipCount(), 1)

	def test_addToManyCarriers(self):
		"""
		Checks that the count of Carriers is one: ships.getCarrierCount()=1	
		"""
		ships = ShipList(self.FIELDLENGTH) # count of Carrier must be 1

		ships.add(Field(0, 0), Field(0, 4))
		self.assertEqual(ships.getCarrierCount(), 1)

		ships.add(Field(1, 1), Field(1, 5))
		self.assertEqual(ships.getCarrierCount(), 1)

	def test_addToManyBattleships(self):
		"""
		Checks that the count of Battleships is two: ships.getBattleshipCount()=2	
		"""		
		ships = ShipList(self.FIELDLENGTH) #count of Battleships must be 2

		ships.add(Field(0, 0), Field(0, 3))
		ships.add(Field(1, 0), Field(1, 3))
		self.assertEqual(ships.getBattleshipCount(), 2)

		ships.add(Field(2, 0), Field(2, 3))
		self.assertEqual(ships.getBattleshipCount(), 2)

	def test_addToManyCruisers(self):
		"""
		Checks that the count of Cruisers is three: ships.getCruiserCount()=3	
		"""
		ships = ShipList(self.FIELDLENGTH) #count of Cruisers must be 3

		ships.add(Field(0, 0), Field(0, 2))
		ships.add(Field(1, 0), Field(1, 2))
		ships.add(Field(2, 0), Field(2, 2))
		self.assertEqual(ships.getCruiserCount(), 3)
		
		ships.add(Field(3, 0), Field(3, 2))
		self.assertEqual(ships.getCruiserCount(), 3)

	def test_addToManyDestroyers(self):
		"""
		Checks that the count of Destroyers is four: ships.getDestroyerCount()=4	
		"""
		ships = ShipList(self.FIELDLENGTH) #count of Destroyers must be 4

		ships.add(Field(0, 0), Field(0, 1))
		ships.add(Field(1, 0), Field(1, 1))
		ships.add(Field(2, 0), Field(2, 1))
		ships.add(Field(3, 0), Field(3, 1))
		self.assertEqual(ships.getDestroyerCount(), 4)

		ships.add(Field(4, 0), Field(4, 1))
		self.assertEqual(ships.getDestroyerCount(), 4)		
#Easy Test#
#---------#
#if __name__ == "__main__":
#	unittest.main()

#Test with detail
# verbosity ist detailgrade
suite = unittest.TestLoader().loadTestsFromTestCase(TestShipList)
unittest.TextTestRunner(verbosity=2).run(suite)  

