import sys
sys.path.append("..")

import unittest
from messageparser import *

class TestMessageParser(unittest.TestCase):

	
	
        ###Server-Messages###
	#----------------------------------------------------------------------------	
	#1x Messages
	#---------------------------------------------------------------------------
	# 11 Begin_Turn
	#format: type:report;status:11;
	def test_beginTurnEncoding(self):
		msg = MessageParser().encode("report",{"status": "11"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		self.assertTrue(msg == "type:report;status:11;")

	def test_beginTurnDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:11;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"11")	

	# 16 Update_Lobby
	#format: type:report;status:16;params;
	#params:
	"""	number_of_clients:[number n];
	   	number_of_games:[number m];
		game_name_0:[name];...;game_name_m-1:[name];
		game_players_count_0:[1|2];...;game_players_m-1:[1|2];
		game_player_0_i:[player_identifier];...;game_player_m-1_i:[player_identifier]   i=0,1
		player_name_0:[name];...;player_name_n-1:[name];
		player_identifier_0:[identifier];...;player_identifier_n-1:[identifier];
	"""
	def test_updateLobbyEncoding(self):
		params={"status": "16", "number_of_clients": "3", "number_of_games": "2", "game_name_0": "FCB",
			"game_name_1": "HSV", "game_players_count_0": "2", "game_players_count_1": "1",
			"game_player_0_0": "1000", "game_player_0_1": "2000", "game_player_1_0": "3000",
			"player_name_0": "Dari","player_name_1": "Max","player_name_2": "",
			"player_identifier_0": "1000", "player_identifier_1": "2000", "player_identifier_2": "3000"}		
		msg = MessageParser().encode("report",params)									
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		#print(msg)
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)

	def test_updateLobbyDecoding(self):
		messageType, params = MessageParser().decode("type:report;"+
							     "status:16;number_of_clients:3;number_of_games:2;game_name_0:FCB;"+
							     "game_name_1:HSV;game_players_count_0:2;game_players_count_1:1;"+
   							     "game_player_0_0:1000;game_player_0_1:2000;game_player_1_0:3000;"+
							     "player_name_0:Dari;player_name_1:Max;player_name_2:;"+
							     "player_identifier_0:1000;player_identifier_1:2000;"+
							     "player_identifier_2:3000;")

		for key,value in params.items():
			print(key+":"+value)		
		self.assertEqual(messageType, "report")
		self.assertEqual(len(params),16 )
		self.assertEqual(params["status"],"16")
		self.assertEqual(params["number_of_games"],"2")
		self.assertEqual(params["number_of_clients"],"3")
		self.assertEqual(params["game_name_0"],"FCB")
		self.assertEqual(params["game_name_1"],"HSV")
		self.assertEqual(params["game_players_count_0"],"2")
		self.assertEqual(params["game_players_count_1"],"1")
		self.assertEqual(params["game_player_0_0"],"1000")
		self.assertEqual(params["game_player_0_1"],"2000")
		self.assertEqual(params["game_player_1_0"],"3000")
		self.assertEqual(params["player_name_0"],"Dari")
		self.assertEqual(params["player_name_1"],"Max")
		self.assertEqual(params["player_name_2"],"")
		self.assertEqual(params["player_identifier_0"],"1000")
		self.assertEqual(params["player_identifier_1"],"2000")
		self.assertEqual(params["player_identifier_2"],"3000")	
			
		
	#17 Game_Ended
	#format: type:report;status:17;params;
	#params:	
	"""	timestamp : [millis] ;
		winner : [0|1] ;
		name_of_game : [name] ;
		identifier_0 : [identifier] ;
		identifier_1 : [identifier] ;
		reason_for_game_end : [text] ;
	"""
	def test_gameEndedEncoding(self):
		params={"status": "17", "timestamp": "1000", "winner": "0", "name_of_game": "FCB",
			"identifier_0": "2000", "identifier_1": "3000", "reason_for_game_end": "player1 won"}		
		msg = MessageParser().encode("report",params)									
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)

	def test_gameEndedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:17;timestamp:1000;winner:0;name_of_game:FCB;"+
						       	     "identifier_0:2000;identifier_1:3000;reason_for_game_end:player1 won")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 7)
		self.assertEqual(params["status"],"17")
		self.assertEqual(params["timestamp"],"1000")
		self.assertEqual(params["winner"],"0")
		self.assertEqual(params["name_of_game"],"FCB")
		self.assertEqual(params["identifier_0"],"2000")
		self.assertEqual(params["identifier_1"],"3000")
		self.assertEqual(params["reason_for_game_end"],"player1 won")	
	
	#13 Update_Own_Field
	#format: type:report;status:13;params;
	#params:
	"""	was_special_attack : [true | false] ;
		coordinate_x : [number] ;
		coordinate_y : [number] ;
	"""	
	def test_updateOwnFieldEncoding(self):
		params={"status": "13", "was_special_attack": "true", "coordinate_x": "12", "coordinate_y":"6"}		
		msg = MessageParser().encode("report",params)									
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)

	def test_updateOwnFieldDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:13;was_special_attack:true;"+
							     "coordinate_x:12;coordinate_y:6;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 4)
		self.assertEqual(params["status"],"13")
		self.assertEqual(params["was_special_attack"],"true")
		self.assertEqual(params["coordinate_x"],"12")
		self.assertEqual(params["coordinate_y"],"6")
	
	#14 Update_Enemy_Field
	#format: type:report;status:14;params;
	#params:
	"""	number_of_updated_fields : [number n] ;
		field_0_x : [number]; ... ; field_n_x : [number];
		field_0_y : [number]; ... ; field_n_y : [number];
		field_0_condition : [free|damaged|undamaged] ; ... ; field_n_condition : [free|damaged|undamaged];
	"""
	def test_updateEnemyFieldEncoding(self):
		params={"status": "14", "number_of_updated_fields": "5", "field_0_x": "3", "field_1_x": "2",
			"field_2_x": "10","field_3_x": "6","field_4_x": "7","field_0_y": "4", "field_1_y": "7",
			"field_2_y": "8","field_3_y": "11","field_4_y": "13","field_0_condition": "free",
			 "field_1_condition": "damaged","field_2_condition": "undamaged","field_3_condition": "free",
			"field_4_condition": "free"}		
		msg = MessageParser().encode("report",params)									
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)

	def test_updateEnemyFieldDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:14;number_of_updated_fields:5;field_0_x:3;"+
							     "field_1_x:2;field_2_x:10;field_3_x:6;field_4_x:7;field_0_y:4;"+
							     "field_1_y:7;field_2_y:8;field_3_y:11;field_4_y:13;field_0_condition:free;"+
			 				     "field_1_condition:damaged;field_2_condition:undamaged;"+
							      "field_3_condition:free;field_4_condition:free")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 17)
		self.assertEqual(params["status"],"14")
		self.assertEqual(params["number_of_updated_fields"],"5")
		self.assertEqual(params["field_0_x"],"3")
		self.assertEqual(params["field_1_x"],"2")
		self.assertEqual(params["field_2_x"],"10")
		self.assertEqual(params["field_3_x"],"6")
		self.assertEqual(params["field_4_x"],"7")
		self.assertEqual(params["field_0_y"],"4")
		self.assertEqual(params["field_1_y"],"7")
		self.assertEqual(params["field_2_y"],"8")
		self.assertEqual(params["field_3_y"],"11")
		self.assertEqual(params["field_4_y"],"13")
		self.assertEqual(params["field_0_condition"],"free")
		self.assertEqual(params["field_1_condition"],"damaged")
		self.assertEqual(params["field_2_condition"],"undamaged")
		self.assertEqual(params["field_3_condition"],"free")
		self.assertEqual(params["field_4_condition"],"free")


	#18 Begin_Ship_Placing
	#format: type:report;status:18;
	def test_beginShipPlacingEncoding(self):
		msg = MessageParser().encode("report",{"status": "18"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string			
		#print ("type"+msg.split("type",1)[1])								
								
		self.assertTrue(msg == "type:report;status:18;")

	def test_beginShipPlacingDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:18;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"18")	
	
	#19 Game_Aborted
	#format: type:report;status:19;
	def test_gameAbortedEncoding(self):
		msg = MessageParser().encode("report",{"status": "19"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
		self.assertTrue(msg == "type:report;status:19;")

	def test_gameAbortedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:19;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"19")
	#----------------------------------------------------------------------------	
	#2x Messages
	#---------------------------------------------------------------------------
	# 21 Successful_Move
	#format: type:report;status:21;
	def test_successfulMoveEncoding(self):
		msg = MessageParser().encode("report",{"status": "21"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:21;")

	def test_successfulMoveDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:21;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"21")

	# 22 Successful_Attack
	#format: type:report;status:22;
	def test_successfulAttackEncoding(self):
		msg = MessageParser().encode("report",{"status": "22"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:22;")

	def test_successfulAttackDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:22;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"22")
	
	# 23 Surrender_Accepted
	#format: type:report;status:23;
	def test_surrenderAcceptedEncoding(self):
		msg = MessageParser().encode("report",{"status": "23"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:23;")

	def test_surrenderAcceptedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:23;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"23")

	# 24 Successful_Special_Attack
	#format: type:report;status:24;
	def test_successfulSpecialAttackEncoding(self):
		msg = MessageParser().encode("report",{"status": "24"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:24;")

	def test_successfulSpecialAttackDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:24;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"24")

	# 27 Successful_Game_Join
	#format: type:report;status:27;
	def test_successfulGameJoinEncoding(self):
		msg = MessageParser().encode("report",{"status": "27"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:27;")

	def test_successfulGameJoinDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:27;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"27")

	# 28 Successful_Game_Create
	#format: type:report;status:28;
	def test_successfulGameCreateEncoding(self):
		msg = MessageParser().encode("report",{"status": "28"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:28;")

	def test_successfulGameCreateDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:28;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"28")

	# 29 Successful_Ship_Placement
	#format: type:report;status:29;
	def test_successfulShipPlacementEncoding(self):
		msg = MessageParser().encode("report",{"status": "29"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:29;")

	def test_successfulShipPlacementDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:29;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"29")
	#----------------------------------------------------------------------------	
	#3x Messages
	#---------------------------------------------------------------------------
	#31 Illegal_Move
	#format: type:report;status:31;
	def test_illegalMoveEncoding(self):
		msg = MessageParser().encode("report",{"status": "31"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:31;")

	def test_illegalMoveDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:31;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"31")

	#32 Illegal_Special_Attack
	#format: type:report;status:32;	
	def test_illegalSpecialAttackEncoding(self):
		msg = MessageParser().encode("report",{"status": "32"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:32;")

	def test_illegalSpecialAttackDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:32;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"32")
	
	#33 Illegal_Field
	#format: type:report;status:33;	
	def test_illegalFieldEncoding(self):
		msg = MessageParser().encode("report",{"status": "33"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:33;")

	def test_illegalFieldDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:33;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"33")

	#34 Illegal_Ship_Index
	#format: type:report;status:34;	
	def test_illegalShipIndexEncoding(self):
		msg = MessageParser().encode("report",{"status": "34"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:34;")

	def test_illegalShipIndexDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:34;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"34")

	#37 Illegal_Game_Definition
	#format: type:report;status:37;	
	def test_illegalGameDefinitionEncoding(self):
		msg = MessageParser().encode("report",{"status": "37"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:37;")

	def test_illegalGameDefinitionDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:37;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"37")
	
	#38 Illegal_Ship_Placement
	#format: type:report;status:38;	
	def test_illegalShipPlacementEncoding(self):
		msg = MessageParser().encode("report",{"status": "38"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:38;")

	def test_illegalShipPlacementDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:38;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"38")
	
	#39 Illegal_Attack
	#format: type:report;status:39;	
	def test_illegalAttackEncoding(self):
		msg = MessageParser().encode("report",{"status": "39"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:39;")

	def test_illegalAttackDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:39;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"39")
	#----------------------------------------------------------------------------	
	#4x Messages
	#---------------------------------------------------------------------------
	#40 Message_Not_Recognized
	#format: type:report;status:40;	
	def test_messageNotRecongnizedEncoding(self):
		msg = MessageParser().encode("report",{"status": "40"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:40;")

	def test_messageNotRecongnizedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:40;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"40")	
	
	#41 Not_Your_Turn
	#format: type:report;status:41;	
	def test_notYourTurnEncoding(self):
		msg = MessageParser().encode("report",{"status": "41"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:41;")

	def test_notYourTurnDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:41;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"41")
		
	#43 Not_In_Any_Game
	#format: type:report;status:43;	
	def test_notInAnyGameEncoding(self):
		msg = MessageParser().encode("report",{"status": "43"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:43;")

	def test_notInAnyGameDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:43;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"43")
	
	#47 Game_Join_Denied
	#format: type:report;status:47;	
	def test_gameJoinDeniedEncoding(self):
		msg = MessageParser().encode("report",{"status": "47"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:47;")

	def test_gameJoinDeniedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:47;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"47")
	
	#48 Game_Preparation_Ended
	#format: type:report;status:48;	
	def test_gamePreparationEndedEncoding(self):
		msg = MessageParser().encode("report",{"status": "48"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:48;")

	def test_gamePreparationEndedDecoding(self):
		messageType, params = MessageParser().decode("type:report;status:48;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"48")
	
	
		
	###Client-Messages###
	#----------------------------------------------------------------------------------------	
	#Lobby Related Messages
	#----------------------------------------------------------------------------------------
	#nickname_set
	#format: type:nickname_set;name:[nickname];
	def test_nickNameSetEncoding(self):
		msg = MessageParser().encode("nickname_set",{"name": "Dari"})				
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string				
					
		self.assertTrue(msg == "type:game_abort;")

	def test_gameAbortDecoding(self):
		messageType, params = MessageParser().decode("type:game_abort;")

		self.assertEqual(messageType, "game_abort")
		self.assertEqual(len(params), 0)
	
				
	#-----------------------------------------------------------------------------------------------------------------------	
	#Game-Related Messages
	#-----------------------------------------------------------------------------------------------------------------------	
	#board_init	
	#format: type:board_init; ship_0_x:[number];ship_0_y:[number];ship_0_direction: [W|E|S|N];...;ship_9_x:[number];ship_9_y:	 
	#[number];ship_9_direction: [W|E|S|N];
	def test_boardInitEncoding(self):
	
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
		
		msg = MessageParser().encode("board_init", params)	 
		msg=msg[2:].decode('utf-8') # decode it from bytes to string		
				
		print (msg)
		# order of parameters is not deterministic
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)			

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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string		
		
						
		self.assertTrue(msg == "type:surrender;")

	def test_surrenderDecoding(self):
		messageType, params = MessageParser().decode("type:surrender;")

		self.assertEqual(messageType, "surrender")
		self.assertEqual(len(params), 0)
		
	#move
	#format: type:move; ship_id:[id];direction:[W|E|S|N];
	def test_moveEncoding(self):
		msg = MessageParser().encode("move", {"ship_id": "5", "direction": "W"})		
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
				
		
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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		
		
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
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
			
		
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
