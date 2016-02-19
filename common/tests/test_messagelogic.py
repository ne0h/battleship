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
	
	"""def setUp(self):  #setup of TestCase 
		
		self.server = TCPServer((self.ServerIP, self.ServerPort), RequestHandler)
		server_thread = threading.Thread(target=self.server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
 
	def tearDown(self): #End of TestCase
		self.server.shutdown()
		self.server.server_close()
	"""
	
	
	
	def test_gameCreateLogic(self):
		
		client1 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Max");
		client2 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"Dari");
	
		#Case 1: Correct create
		GameName="FCB"
		cb1 = Callback()		
		cb1.onAction = lambda success: self.__onCreateGame(success,1)
		client1.createGame(GameName,cb1)
	
		#Case 2: Too long gamename
		GameName="x"*100
		cb2 = Callback()	
		cb2.onAction = lambda success: self.__onCreateGame(success,2)
		client2.createGame(GameName,cb2)

		#Case 3: Create with same name
		GameName="FCB"
		cb2 = Callback()	
		cb2.onAction = lambda success: self.__onCreateGame(success,3)
		client2.createGame(GameName,cb2)
		
		#Case 4: Create again after a successful create of same player
		GameName="Berlin"
		cb1 = Callback()		
		cb1.onAction = lambda success: self.__onCreateGame(success,4)
		client1.createGame(GameName,cb1)
		
		client1.leaveGame(cb1)
		client2.leaveGame(cb2)


	def __onCreateGame(self, success, case):
		
		if case==1:
			if success:
				print("case:"+str(case)+":success")
				self.assertTrue(True)
			else: 
				print("case:"+str(case)+":fail")
				self.assertTrue(False)
		else:
			if  success:
				print("case:"+str(case)+":success")
				self.assertTrue(False)
			else: 
				print("fail")
				print("case:"+str(case)+":fail")
				self.assertTrue(True)
	
		

	"""
	def test_gameJoinLogic(self):
		
		client1 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client1.connect("",self.ServerIP,self.ServerPort)
		client2 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client2.connect("Max",self.ServerIP,self.ServerPort)
		client3 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client3.connect("Dari",self.ServerIP,self.ServerPort)
	
		client1.joinGame(None)
		self.assertEqaul(success,True)
		client2.joinGame(None)
		self.assertEqaul(success,True)
		
	def test_gameAbortLogic(self):
		
		client1 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client1.connect("",self.ServerIP,self.ServerPort)
		client2 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client2.connect("Max",self.ServerIP,self.ServerPort)
		client3 = Backend(self.FIELDLENGTH,self.ServerIP,self.ServerPort,"");
		client3.connect("Dari",self.ServerIP,self.ServerPort)
	
		client1.leaveGame(None)
		self.assertEqaul(success,True)
		client2.leaveGame(None)
		self.assertEqaul(success,True)
	"""
if __name__ == "__main__":
	unittest.main()
