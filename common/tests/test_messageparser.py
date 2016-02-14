import sys
sys.path.append("..")

import unittest
from messageparser import *

class TestMessageParser(unittest.TestCase):

	#Lobby Related Messages
	#----------------------------------------------------------------------------------------
	#nickname_set
	#format: type:nickname_set;name:[nickname];
	def test_nickNameSetEncoding(self):
		msg = MessageParser().encode("nickname_set",{"name": "Dari"})				
		msg=msg.decode('utf-8') # decode it from bytes to string						
		msg = msg[2:] 		# we don't want first character				
		self.assertTrue(msg == "type:nickname_set;name:Dari;")

	def test_nickNameSetDecoding(self):
		messageType, params = MessageParser().decode("type:nickname_set;name:Dari;")

		self.assertEqual(messageType, "nickname_set")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"Dari")	
	
	#game_create
	#format: type:game_create;name:[name];
	def test_gameCreateEncoding(self):
		msg = MessageParser().encode("game_create",{"name": "FCB"})				
		msg=msg.decode('utf-8') # decode it from bytes to string						
		msg = msg[2:] 		# we don't want first character				
		self.assertTrue(msg == "type:game_create;name:FCB;")

	def test_gameCreateDecoding(self):
		messageType, params = MessageParser().decode("type:game_create;name:FCB;")

		self.assertEqual(messageType, "game_create")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"FCB")
	
	#game_join
	#format: type:game_join;name:[name];	
	def test_gameJoinEncoding(self):
		msg = MessageParser().encode("game_join",{"name": "FCB"})				
		msg=msg.decode('utf-8') # decode it from bytes to string						
		msg = msg[2:] 		# we don't want first character				
		self.assertTrue(msg == "type:game_join;name:FCB;")

	def test_gameJoinDecoding(self):
		messageType, params = MessageParser().decode("type:game_join;name:FCB;")

		self.assertEqual(messageType, "game_join")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"FCB")

	#game_abort
	#format: type:game_abort;
	def test_gameAbortEncoding(self):
		msg = MessageParser().encode("game_abort",{})				
		msg=msg.decode('utf-8') # decode it from bytes to string				
		msg = msg[2:] 		# we don't want first character			
		self.assertTrue(msg == "type:game_abort;")

	def test_gameAbortDecoding(self):
		messageType, params = MessageParser().decode("type:game_abort;")

		self.assertEqual(messageType, "game_abort")
		self.assertEqual(len(params), 0)
	
	#chat_send
	#format: type:chat_send;text:[text];
	def test_chatSendEncoding(self):
		msg = MessageParser().encode("chat_send",{"text": "How are you?"})				
		msg=msg.decode('utf-8') # decode it from bytes to string				
		msg = msg[2:] 		# we don't want first character				
		self.assertTrue(msg == "type:chat_send;text:How are you?;")

	def test_chatSendDecoding(self):
		messageType, params = MessageParser().decode("type:chat_send;text:How are you?;")

		self.assertEqual(messageType, "chat_send")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["text"],"How are you?")
	#-----------------------------------------------------------------------------------------------------------------------	
	#Game-Related Messages
	#-----------------------------------------------------------------------------------------------------------------------	
	#board_init	
	#format: type:board_init; ship_0_x:[number];ship_0_y:[number];ship_0_direction: [W|E|S|N];...;ship_9_x:[number];ship_9_y:	 
	#[number];ship_9_direction: [W|E|S|N];
	def test_boardInitEncoding(self):

		#for max:please change your messageparser
		# if you use set we have 30! permutation (it is impossible to check all)		
		params = {"ship_0_x": "5", "ship_0_y": "3", "ship_0_direction": "W",
			  "ship_1_x": "6", "ship_1_y": "3", "ship_1_direction": "N",
		          "ship_2_x": "4", "ship_2_y": "2", "ship_2_direction": "E",
		          "ship_3_x": "7", "ship_3_y": "3", "ship_3_direction": "N",
		          "ship_4_x": "8", "ship_4_y": "3", "ship_4_direction": "N",
			  "ship_5_x": "9", "ship_5_y": "3", "ship_5_direction": "N",
		          "ship_6_x": "12", "ship_6_y": "3", "ship_6_direction": "W",
			  "ship_7_x": "10", "ship_7_y": "4", "ship_7_direction": "N",
			  "ship_8_x": "10", "ship_8_y": "8", "ship_8_direction": "E",
			  "ship_9_x": "12", "ship_9_y": "8", "ship_9_direction": "S" }
		#by List you have 1 permutation		
		params2 = ["ship_0_x:5", "ship_0_y:3", "ship_0_direction:W",
			  "ship_1_x:6", "ship_1_y:3", "ship_1_direction:N",
		          "ship_2_x:4", "ship_2_y:2", "ship_2_direction:E",
		          "ship_3_x:7", "ship_3_y:3", "ship_3_direction:N",
		          "ship_4_x:8", "ship_4_y:3", "ship_4_direction:N",
			  "ship_5_x:9", "ship_5_y:3", "ship_5_direction:N",
		          "ship_6_x:12", "ship_6_y:3", "ship_6_direction:W",
			  "ship_7_x:10", "ship_7_y:4", "ship_7_direction:N",
			  "ship_8_x:10", "ship_8_y:8", "ship_8_direction:E",
			  "ship_9_x:12", "ship_9_y:8", "ship_9_direction:S"]	
		# by list of sets you have 10*3!=60  permutation		
		params3= [{"ship_0_x": "5", "ship_0_y": "3", "ship_0_direction": "W"},
			  {"ship_1_x": "6", "ship_1_y": "3", "ship_1_direction": "N"},
		          {"ship_2_x": "4", "ship_2_y": "2", "ship_2_direction": "E"},
		          {"ship_3_x": "7", "ship_3_y": "3", "ship_3_direction": "N"},
		          {"ship_4_x": "8", "ship_4_y": "3", "ship_4_direction": "N"},
			  {"ship_5_x": "9", "ship_5_y": "3", "ship_5_direction": "N"},
		          {"ship_6_x": "12", "ship_6_y": "3", "ship_6_direction": "W"},
			  {"ship_7_x": "10", "ship_7_y": "4", "ship_7_direction": "N"},
			  {"ship_8_x": "10", "ship_8_y": "8", "ship_8_direction": "E"},
			  {"ship_9_x": "12", "ship_9_y": "8", "ship_9_direction": "S"} ]	
		"""print (params)	
		print (params2)
		print (params3)	
		msg = MessageParser().encode("board_init", params)	
		print (msg) 
		msg=msg.decode('utf-8') # decode it from bytes to string		
		msg = msg[2:] 		# we don't want first character		
		print (msg)
		# order of parameters is not deterministic
						
		self.assertTrue(msg == "type:move;direction:W;ship_id:5;" or
				msg== "type:move;ship_id:5;direction:W;")"""
		self.assertTrue(False)

	def test_boardInitDecoding(self):
		messageType, params = MessageParser().decode("type:board_init;"+
							    "ship_0_x:5;ship_0_y:3;ship_0_direction:W;"+ 
							    "ship_1_x:6;ship_1_y:3;ship_1_direction:N;"+
							    "ship_2_x:4;ship_2_y:2;ship_2_direction:E;"+
							    "ship_3_x:7;ship_3_y:3;ship_3_direction:N;"+
							    "ship_4_x:8;ship_4_y:3;ship_4_direction:N;"+
							    "ship_5_x:9;ship_5_y:3;ship_5_direction:N;"+
							    "ship_6_x:12;ship_6_y:3;ship_6_direction:W;"+
							    "ship_7_x:10;ship_7_y:4;ship_7_direction:N;"+
							    "ship_8_x:10;ship_8_y:8;ship_8_direction:E;"+
							    "ship_9_x:12;ship_9_y:8;ship_9_direction:S;")

		self.assertEqual(messageType, "board_init")
		self.assertEqual(len(params), 30)
		
		self.assertEqual(params["ship_0_x"], "5")		# integers are strings at this step
		self.assertEqual(params["ship_0_y"], "3")
		self.assertEqual(params["ship_0_direction"],"W")

		self.assertEqual(params["ship_1_x"], "6")		
		self.assertEqual(params["ship_1_y"], "3")
		self.assertEqual(params["ship_1_direction"],"N")

		self.assertEqual(params["ship_2_x"], "4")		
		self.assertEqual(params["ship_2_y"], "2")
		self.assertEqual(params["ship_2_direction"],"E")

		self.assertEqual(params["ship_3_x"], "7")		
		self.assertEqual(params["ship_3_y"], "3")
		self.assertEqual(params["ship_3_direction"],"N")

		self.assertEqual(params["ship_4_x"], "8")		
		self.assertEqual(params["ship_4_y"], "3")
		self.assertEqual(params["ship_4_direction"],"N")

		self.assertEqual(params["ship_5_x"], "9")		
		self.assertEqual(params["ship_5_y"], "3")
		self.assertEqual(params["ship_5_direction"],"N")

		self.assertEqual(params["ship_6_x"], "12")		
		self.assertEqual(params["ship_6_y"], "3")
		self.assertEqual(params["ship_6_direction"],"W")

		self.assertEqual(params["ship_7_x"], "10")		
		self.assertEqual(params["ship_7_y"], "4")
		self.assertEqual(params["ship_7_direction"],"N")

		self.assertEqual(params["ship_8_x"], "10")		
		self.assertEqual(params["ship_8_y"], "8")
		self.assertEqual(params["ship_8_direction"],"E")

		self.assertEqual(params["ship_9_x"], "12")		
		self.assertEqual(params["ship_9_y"], "8")
		self.assertEqual(params["ship_9_direction"],"S")	
	
	#surrender
	#format: type:surrender;
	def test_surrenderEncoding(self):
		msg = MessageParser().encode("surrender",{})		
		msg=msg.decode('utf-8') # decode it from bytes to string		
		msg = msg[2:] 		# we don't want first character
						
		self.assertTrue(msg == "type:surrender;")

	def test_surrenderDecoding(self):
		messageType, params = MessageParser().decode("type:surrender;")

		self.assertEqual(messageType, "surrender")
		self.assertEqual(len(params), 0)
		
	#move
	#format: type:move; ship_id:[id];direction:[W|E|S|N];
	def test_moveEncoding(self):
		msg = MessageParser().encode("move", {"ship_id": "5", "direction": "W"})		
		msg=msg.decode('utf-8') # decode it from bytes to string
		msg = msg[2:] 		# we don't want first character		
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:move;direction:W;ship_id:5;" or
				msg== "type:move;ship_id:5;direction:W;")

	def test_moveDecoding(self):
		messageType, params = MessageParser().decode("type:move; ship_id:5; direction:W;")

		self.assertEqual(messageType, "move")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["ship_id"], "5")		# integers are strings at this step
		self.assertEqual(params["direction"], "W")	

	#attack
	#format: type:attack;coordinate_x:[number];coordinate_y:[number];
	def test_attackEncoding(self):
		msg = MessageParser().encode("attack", {"coordinate_x": "5", "coordinate_y": "14"})
		msg=msg.decode('utf-8') # decode it from bytes to string
		msg = msg[2:] 		# we don't want first character
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:attack;coordinate_y:14;coordinate_x:5;" or
				msg== "type:attack;coordinate_x:5;coordinate_y:14;")

	def test_attackDecoding(self):
		messageType, params = MessageParser().decode("type:attack; coordinate_x:5; coordinate_y:14;")

		self.assertEqual(messageType, "attack")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["coordinate_x"], "5")		# integers are strings at this step
		self.assertEqual(params["coordinate_y"], "14")
	
	# special_attack
	#Format: type:special_attack;coordinate_x:[number];coordinate_y:[number]; 
	def test_attackSpecialEncoding(self):
		msg = MessageParser().encode("special_attack", {"coordinate_x": "5", "coordinate_y": "14"})
		msg=msg.decode('utf-8') # decode it from bytes to string
		msg = msg[2:] 		# we don't want first character	
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:special_attack;coordinate_y:14;coordinate_x:5;" or
				msg== "type:special_attack;coordinate_x:5;coordinate_y:14;")

	def test_attackSpecialDecoding(self):
		messageType, params = MessageParser().decode("type:special_attack; coordinate_x:5; coordinate_y:14;")

		self.assertEqual(messageType, "special_attack")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["coordinate_x"], "5")		# integers are strings at this step
		self.assertEqual(params["coordinate_y"], "14")
	

if __name__ == "__main__":
	unittest.main()
