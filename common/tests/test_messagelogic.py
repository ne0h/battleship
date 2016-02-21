import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../client')) # 2 times up 
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # 1 time up
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))
#import client
#import server
from backend import *
from lobby import *

import unittest

class TestMessageLogic(unittest.TestCase):
	
	
	ServerIP="localhost"
	ServerPort=12345
	FIELDLENGTH = 16
	clients =[]
	callbacks=[]
	
	"""def setUp(self):  #setup of TestCase 
		
		self.server = TCPServer((self.ServerIP, self.ServerPort), RequestHandler)
		server_thread = threading.Thread(target=self.server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
 	
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
		self.callbacks[1]=cb2
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
	
		#Case 1: Correct join
		GameName="FCB"
		cb1 = Callback()
		self.callbacks[1]=cb1	
		self.callbacks[1].onAction = lambda success: self.__onJoinGame(success,1)
		self.clients[1].joinGame(GameName,self.callbacks[1])
		
		#Case 2: Join a full room 
		GameName="FCB"
		cb3 = Callback()
		self.callbacks.append(cb3)	
		self.callbacks[2].onAction = lambda success: self.__onJoinGame(success,2)
		self.clients[2].joinGame(GameName,self.callbacks[2])

		"""
		#Case 3: Gamename doesn't exist
		GameName="Berlin"
		cb3 = Callback()	
		cb3.onAction = lambda success: self.__onJoinGame(success,2)
		self.clients[2].joinGame(GameName,cb3)

		
		#Case 4: multiple join of same player
		GameName="Berlin"
		cb1 = Callback()		
		cb1.onAction = lambda success: self.__onCreateGame(success,4)
		client1.createGame(GameName,cb1)
		"""

	def __onJoinGame(self, success,case):
		#case 1 and 2 have a race condition
		if(success): 
				case=1
		elif case<3:
				case=2

		if case==1:
			if success:
				print("In JoinGame case:"+str(case)+":success")
				self.assertTrue(True)
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
	
if __name__ == "__main__":
	unittest.main()
