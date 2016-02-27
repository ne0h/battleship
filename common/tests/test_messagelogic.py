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

class TestMessageLogic(unittest.TestCase):
	
	
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

	def test_03_moveLogic(self):
		
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
		"""
		print("Clients 0 ships")
		ships=self.clients[0].getOwnShips()
		for ship in ships:
			print("ship_bow: (" + str(ship.bow.x)+"," +str(ship.bow.y)+ ") ship_rear:(" +str(ship.rear.x)+","+str(ship.rear.y)+")") 

		print("Clients 1 ships")
		ships=self.clients[1].getOwnShips()
		for ship in ships:
			print("ship_bow: (" + str(ship.bow.x)+"," +str(ship.bow.y)+ ") ship_rear:(" +str(ship.rear.x)+","+str(ship.rear.y)+")")
		"""
		self.controll=0
		while(self.controll==0):
			if (self.clients[0].clientStatus==ClientStatus.OWNTURN):
				 self.controll=1
				 self.turn =0
			elif (self.clients[1].clientStatus==ClientStatus.OWNTURN):
				self.controll=1
				self.turn=1

		if(self.turn==0):
			print("First Turn is for client 0")
		elif(self.turn==1):
			print("First Turn is for client 1")

		#Orientation.NORTH: "N",
		#Orientation.WEST:  "W",
		#Orientation.SOUTH: "S",
		#Orientation.EAST:  "E"
		
		if (self.turn==0):
			#Case 1: Correct move
			success=self.clients[0].move(6,Orientation.NORTH)
			self.__onMove(success,1)
			
			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			#Case 2: wrong index
			success=self.clients[1].move(10,Orientation.NORTH)
			self.__onMove(success,2)

			#Case 3: out of boundry
			success=self.clients[1].move(6,Orientation.WEST)
			self.__onMove(success,3)

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue
		
		elif (self.turn==1):
			#Case 1: Correct move
			success=self.clients[1].move(6,Orientation.NORTH)
			self.__onMove(success,1)
			
			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			#Case 2: wrong index
			success=self.clients[0].move(10,Orientation.NORTH)
			self.__onMove(success,2)

			#Case 3: out of boundry
			success=self.clients[0].move(6,Orientation.WEST)
			self.__onMove(success,3)

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue
			
		
	def __onMove(self, success,case):

		if case==1:
			if success:
				print("In Move case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)
			else: 
				print("In Move case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(False)
		else:
			if success:
				print("In Move case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(False)
			else: 
				print("In Move case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)

	def test_04_attackLogic(self):
		
		print("-----------------------------------------")
		print("In AttackLogic ClientStatus 0:"+str(self.clients[0].clientStatus))	
		print("In AttackLogic ClientStatus 1:"+str(self.clients[1].clientStatus))
		
		if (self.clients[0].clientStatus==ClientStatus.OWNTURN):
			self.turn =0
		elif (self.clients[1].clientStatus==ClientStatus.OWNTURN):
			self.turn=1

		print("Turn in AttackLogic:"+str(self.turn))

		cb1 = Callback()
		self.callbacks.pop(0)
		self.callbacks.insert(0,cb1)

		cb2 = Callback()
		self.callbacks.pop(1)
		self.callbacks.insert(1,cb2)

		if (self.turn==0):
			#Case 1: Correct attack
			self.clients[0].registerGamePlayCallback(self.callbacks[0])
			self.callbacks[0].onAction = lambda status: self.__onAttack(status,1)
			self.clients[0].attack(Field(4,4))

			while(self.clients[1].clientStatus!=ClientStatus.OWNTURN):
				continue

			#Case 2: out of boundry
			self.clients[1].registerGamePlayCallback(self.callbacks[1])
			self.callbacks[1].onAction = lambda status: self.__onAttack(status,2)
			self.clients[1].attack(Field(-1,1))

			while(self.clients[0].clientStatus==ClientStatus.OWNTURN):
				continue

		
		elif (self.turn==1):	
			#Case 1: Correct attack
			self.clients[1].registerGamePlayCallback(self.callbacks[1])
			self.callbacks[1].onAction = lambda status: self.__onAttack(status,1)
			self.clients[1].attack(Field(4,4))

			while(self.clients[0].clientStatus!=ClientStatus.OWNTURN):
				continue

			#Case 2: out of boundry
			self.clients[0].registerGamePlayCallback(self.callbacks[0])
			self.callbacks[0].onAction = lambda status: self.__onAttack(status,2)
			self.clients[0].attack(Field(-1,1))

			while(self.clients[1].clientStatus==ClientStatus.OWNTURN):
				continue
	

	def __onAttack(self, status,case):
		
		if case==1:
			if status is 22:
				print("In Attack case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)
			else: 
				print("In Attack case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(False)
		else:
			if  status is 39:
				print("In Attack case:"+str(case)+":fail")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(True)
			
			else: 
				print("In Attack case:"+str(case)+":success")
				print("ClientStatus 0:"+str(self.clients[0].clientStatus))	
				print("ClientStatus 1:"+str(self.clients[1].clientStatus))
				self.assertTrue(false)
	
	
    	
if __name__ == "__main__":
	unittest.main()
