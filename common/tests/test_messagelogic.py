import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../client')) # 2 times up 
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # 1 time up
from backend import *
from lobby import *

import unittest

class TestMessageLogic(unittest.TestCase):
	
	
	ServerIP="localhost"
	ServerPort=12345
	FIELDLENGTH = 16
	clients =[]
	callbacks=[]
	controll=0
	
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

	def test_gameCreateLogic(self):
		
		client1 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Max");
		client2 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Dari");
		
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
	

	def test_gameJoinLogic(self):
		
		client3 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Yonis");
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

	def test_moveLogic(self):
		
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

		ships=self.clients[0].getOwnShips()
		for ship in ships:
			print("ship_bow: (" + str(ship.bow.x)+"," +str(ship.bow.y)+ ") ship_rear:(" +str(ship.rear.x)+","+str(ship.rear.y)+")") 
		
		#Case 1: Correct move
		# 0:N 1:W 2:S 3:E		
		success=self.clients[0].move(6,0)
		self.__onMove(success,1)
		

		#Case 2: wrong index
		success=self.clients[1].move(10,0)
		self.__onMove(success,2)
		

		#Case 3: out of boundry
		success=self.clients[1].move(6,1)
		self.__onMove(success,3)
		
	def __onMove(self, success,case):
		
		if case==1:
			if success:
				print("In Move case:"+str(case)+":success")
				self.assertTrue(True)
			else: 
				print("In Move case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("In Move case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("In Move case:"+str(case)+":fail")
				self.assertTrue(True)

	def test_attackLogic(self):
		

		#Case 1: Correct attack
		self.clients[1].attack(Field(4,4))

		#Case 2: out of boundry
		self.clients[0].attack(-1,1)
		
	def __onAttack(self, success,case):
		
		if case==1:
			if success:
				print("In Attack case:"+str(case)+":success")
				self.assertTrue(True)
			else: 
				print("In Attack case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("In Attack case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("In Attack case:"+str(case)+":fail")
				self.assertTrue(True)

	def test_specialAttackLogic(self):
		

		#Case 1: Correct attack
		self.clients[0].specialAttack(Field(3,3))

		#Case 2: out of boundry
		self.clients[1].attack(-1,1)

		#Case 3: More than 3 Special Attacks
		self.clients[1].specialAttack(5,6)
		self.clients[0].specialAttack(9,6)
		self.clients[1].attack(5,6)
		self.clients[0].specialAttack(10,12)
		self.clients[1].attack(8,6)
		self.clients[0].specialAttack(12,12) 		
		
	def __onSpecialAttack(self, success,case):
		
		if case==1:
			if success:
				print("In SpecialAttack case:"+str(case)+":success")
				self.assertTrue(True)
			else: 
				print("In SpecialAttack case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("In SpecialAttack case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("In SpecialAttack case:"+str(case)+":fail")
				self.assertTrue(True)


if __name__ == "__main__":
	unittest.main()
