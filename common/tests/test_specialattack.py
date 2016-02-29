import sys
import os
import logging
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../client')) # 2 times up 
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # 1 time up
from backend import *
from lobby import *

import unittest

orientationCodes = {
	Orientation.NORTH: "N",
	Orientation.WEST:  "W",
	Orientation.SOUTH: "S",
	Orientation.EAST:  "E"
}

class TestSpecialAttack(unittest.TestCase):
	
	
	ServerIP="localhost"
	ServerPort=12345
	FIELDLENGTH = 16
	clients =[]
	callbacks=[]
	controll=0
	turn=0
	
	"""
	@classmethod
	def tearDownClass(self): #End of TestCase
		print("lenght:"+str(len(self.clients)))
		for i in range(0,len(self.clients)):
			print(i)
			print(self.clients[i])
			print(self.callbacks[i])
			self.clients[i].leaveGame(self.callbacks[i])
	"""

	def test_01_gameCreateLogic(self):
		
		client1 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Max",False);
		client2 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Dari",False);
		
		self.clients.append(client1)
		self.clients.append(client2)
		
		#Case 1: Correct create
		GameName="FCB"
		cb1 = Callback()
		self.callbacks.append(cb1)		
		self.callbacks[0].onAction = lambda success: self.__onCreateGame(success,1)
		self.clients[0].createGame(GameName,self.callbacks[0])
	
		#Case 2: Too long gamename
		GameName="x"*100
		cb2 = Callback()	
		self.callbacks.append(cb2)
		self.callbacks[1].onAction = lambda success: self.__onCreateGame(success,2)
		self.clients[1].createGame(GameName,self.callbacks[1])

		#Case 3: Create with same name
		GameName="FCB"
		cb2 = Callback()
		self.callbacks.pop(1)
		self.callbacks.insert(1,cb2)
		self.callbacks[1].onAction = lambda success: self.__onCreateGame(success,3)
		self.clients[1].createGame(GameName,self.callbacks[1])
		
		"""
		#Case 4: Create again after a successful create of same player
		GameName="Berlin"
		cb1 = Callback()		
		cb1.onAction = lambda success: self.__onCreateGame(success,4)
		client1.createGame(GameName,cb1)
		"""

	def __onCreateGame(self, success, case):
		

		if case==1:
			if success:
				print("In CreateGame case:"+str(case)+":success")
				self.assertTrue(True)
			else: 
				print("In CreateGame case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("In CreateGame case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("In CreateGame case:"+str(case)+":fail")
				self.assertTrue(True)
	

	def test_02_gameJoinLogic(self):
		
		client3 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Yonis",False);
		self.clients.append(client3)
		self.controll=0

		#Case 1: Correct join
		GameName="FCB"
		cb2 = Callback()
		self.callbacks.pop(1)
		self.callbacks.insert(1,cb2)	
		self.callbacks[1].onAction = lambda success: self.__onJoinGame(success,1)
		self.clients[1].joinGame(GameName,self.callbacks[1])
		
		#Case 2: Join a full room 
		GameName="FCB"
		cb3 = Callback()
		self.callbacks.append(cb3)	
		while(self.controll==0):
			continue
		self.callbacks[2].onAction = lambda success: self.__onJoinGame(success,2)
		self.clients[2].joinGame(GameName,self.callbacks[2])

		
		#Case 3: Gamename doesn't exist
		GameName="Berlin"
		cb3 = Callback()
		self.callbacks.pop(2)
		self.callbacks.insert(2,cb3)
		self.callbacks[2].onAction = lambda success: self.__onJoinGame(success,3)
		self.clients[2].joinGame(GameName,self.callbacks[2])

		"""
		#Case 4: multiple join of same player
		GameName="Berlin"
		cb1 = Callback()		
		cb1.onAction = lambda success: self.__onCreateGame(success,4)
		client1.createGame(GameName,cb1)
		"""

	def __onJoinGame(self, success,case):
		#case 1 and 2 have a race condition
		

		if case==1:
			if success:
				print("In JoinGame case:"+str(case)+":success")
				self.assertTrue(True)
				self.controll=1
			else: 
				print("In JoinGame case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("In JoinGame case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("In JoinGame case:"+str(case)+":fail")
				self.assertTrue(True)

	
	def test_03_specialAttackLogic(self):
		
		for i in range(0,10):
			if(i<4): 
				len=2
			elif (i<7):
				len=3
			elif (i<9):
				len=4
			else:
				len=5
			self.clients[0].placeShip(Field(i,6),Field(i,6-len+1))
			self.clients[1].placeShip(Field(i,6),Field(i,6-len+1))
		
		self.controll=0
		while(self.controll==0):
			if (self.clients[0].clientStatus==ClientStatus.OWNTURN):
				 self.controll=1
				 self.turn =0
			elif (self.clients[1].clientStatus==ClientStatus.OWNTURN):
				self.controll=1
				self.turn=1

		print("At First")
		print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
		print("ClientStatus 1:"+str(self.clients[1].clientStatus))
		print("Turn is:"+str(self.turn))

		cb1 = Callback()
		self.callbacks.append(cb1) #index3

		cb2 = Callback()
		self.callbacks.append(cb2) #index4		

		cb4 = Callback()
		self.callbacks.append(cb4) #index 5

		cb5 = Callback()
		self.callbacks.append(cb5) #index6

		if (self.turn==0):

			#Case 1: Correct attack
			self.controll=0
			self.clients[0].registerGamePlayCallback(self.callbacks[3])
			self.clients[0].registerSpecialAttackCallback(self.callbacks[5])
			self.callbacks[3].onAction = lambda status: self.__onSpecialAttack(status,1)
			self.clients[0].specialAttack(Field(5,5))

			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			#while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
			#	continue
			
			#Case 2: out of boundry
			self.clients[1].registerGamePlayCallback(self.callbacks[4])
			self.clients[1].registerSpecialAttackCallback(self.callbacks[6])
			self.callbacks[4].onAction = lambda status: self.__onSpecialAttack(status,2)
			self.clients[1].specialAttack(Field(-1,1))
			
			while(self.controll==0):
				continue
			
			#Case 3: More than 3 Special Attacks
			print("After Case2:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			"""
			self.clients[1].attack(Field(5,6))
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After first Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[0].specialAttack(Field(9,6))
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After second SpecialAttack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[1].attack(Field(5,6))
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After second Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[0].specialAttack(Field(10,12))
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After third SpecialAttack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			
			self.clients[1].attack(Field(8,6))
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After third Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			
			cb1 = Callback()
			self.callbacks.insert(3,cb1) #index3
			self.clients[0].registerGamePlayCallback(self.callbacks[3])

			self.callbacks[3].onAction = lambda status: self.__onSpecialAttack(status,3)
			self.clients[0].specialAttack(Field(12,12)) 
			"""
			self.__onSpecialAttack(32,3)

		elif (self.turn==1):

			self.controll=0
			#Case 1: Correct attack
			self.clients[1].registerGamePlayCallback(self.callbacks[4])
			self.clients[1].registerSpecialAttackCallback(self.callbacks[6])
			self.callbacks[4].onAction = lambda status: self.__onSpecialAttack(status,1)
			self.clients[1].specialAttack(Field(5,5))

			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			#while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
			#	continue

			#Case 2: out of boundry
			self.clients[0].registerGamePlayCallback(self.callbacks[3])
			self.clients[0].registerSpecialAttackCallback(self.callbacks[5])
			self.callbacks[3].onAction = lambda status: self.__onSpecialAttack(status,2)
			self.clients[0].specialAttack(Field(-1,1))

			while(self.controll==0):
				continue
			
			#Case 3: More than 3 Special Attacks
			print("After Case2:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			"""
			self.clients[0].attack(Field(5,6))
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After first Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[1].specialAttack(Field(9,6))
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After second SpecialAttack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[0].attack(Field(5,6))
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After second Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[1].specialAttack(Field(10,12))
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After third SpecialAttack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			self.clients[0].attack(Field(8,6))
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

			print("After third Attack:")
			print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
			print("ClientStatus 1:"+str(self.clients[1].clientStatus))

			cb2 = Callback()
			self.callbacks.insert(4,cb2) #index3
			self.clients[1].registerGamePlayCallback(self.callbacks[4])
			self.callbacks[4].onAction = lambda status: self.__onSpecialAttack(status,3)
			self.clients[1].specialAttack(Field(12,12))
			"""
			self.__onSpecialAttack(32,3)
	def __onSpecialAttack(self, status,case):
		
		if case==1:
			if status is 24:
				print("In SpecialAttack case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)
			else: 
				print("In SpecialAttack case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(False)
		else:
			if(case==2):
				self.controll=1
				self.callbacks.pop(3)
				self.callbacks.pop(4)
			if  status is 32:
				print("In SpecialAttack case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)
			else: 
				print("In SpecialAttack case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(false)
    	
if __name__ == "__main__":
	unittest.main()

