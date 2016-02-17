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
	def test_beginTurnEncoding(self):
		"""
		Checks the Encoding of 11 Begin_Turn Message by MessageParser
		Format:
			 type:report;status:11;
		"""
		msg = MessageParser().encode("report",{"status": "11"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		self.assertTrue(msg == "type:report;status:11;")

	def test_beginTurnDecoding(self):
		"""
		Checks the Decoding of 11 Begin_Turn Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:11;")
		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"11")	

	# 16 Update_Lobby
	def test_updateLobbyEncoding(self):
		"""
		Checks the Encoding of 16 Update_Lobby Message by MessageParser
		Format: 
			type:report;status:16;params;
		params:
			number_of_clients:[number n];
	   		number_of_games:[number m];
			game_name_0:[name];...;game_name_m-1:[name];
			game_players_count_0:[1|2];...;game_players_m-1:[1|2];
			game_player_0_i:[player_identifier];...;game_player_m-1_i:[player_identifier]   i=0,1
			player_name_0:[name];...;player_name_n-1:[name];
			player_identifier_0:[identifier];...;player_identifier_n-1:[identifier];
		"""
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
		"""
		Checks the Decoding of 16 Update_Lobby Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;"+
							     "status:16;number_of_clients:3;number_of_games:2;game_name_0:FCB;"+
							     "game_name_1:HSV;game_players_count_0:2;game_players_count_1:1;"+
   							     "game_player_0_0:1000;game_player_0_1:2000;game_player_1_0:3000;"+
							     "player_name_0:Dari;player_name_1:Max;player_name_2:;"+
							     "player_identifier_0:1000;player_identifier_1:2000;"+
							     "player_identifier_2:3000;")
	
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
	def test_gameEndedEncoding(self):
		"""
		Checks the Encoding of 17 Game_Ended Message by MessageParser 	
		Format: 
			type:report;status:17;params;
		params:	
			timestamp : [millis] ;
			winner : [0|1] ;
			name_of_game : [name] ;
			identifier_0 : [identifier] ;
			identifier_1 : [identifier] ;
			reason_for_game_end : [text] ;
		"""
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
		"""
		Checks the Decoding of 17 Game_Ended Message by MessageParser
		"""		
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
	def test_updateOwnFieldEncoding(self):
		"""
		Checks the Encoding of 13 Update_Own_Field Message by MessageParser
		Format: 
			type:report;status:13;params;
		params:
			was_special_attack : [true | false] ;
			coordinate_x : [number] ;
			coordinate_y : [number] ;
		"""	
		params={"status": "13", "was_special_attack": "true", "coordinate_x": "12", "coordinate_y":"6"}		
		msg = MessageParser().encode("report",params)									
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)

	def test_updateOwnFieldDecoding(self):
		"""
		Checks the Decoding of 13 Update_Own_Field Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:13;was_special_attack:true;"+
							     "coordinate_x:12;coordinate_y:6;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 4)
		self.assertEqual(params["status"],"13")
		self.assertEqual(params["was_special_attack"],"true")
		self.assertEqual(params["coordinate_x"],"12")
		self.assertEqual(params["coordinate_y"],"6")
	
	#14 Update_Enemy_Field
	def test_updateEnemyFieldEncoding(self):
		"""
		Checks the Encoding of 14 Update_Enemy_Field Message by MessageParser
		Format: 
			type:report;status:14;params;
		params:
			number_of_updated_fields : [number n] ;
			field_0_x : [number]; ... ; field_n_x : [number];
			field_0_y : [number]; ... ; field_n_y : [number];
			field_0_condition : [free|damaged|undamaged] ; ... ; field_n_condition : [free|damaged|undamaged];
		"""
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
		"""
		Checks the Decoding of 14 Update_Enemy_Field Message by MessageParser
		"""	
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
	def test_beginShipPlacingEncoding(self):
		""" 	
		Checks the Encoding of 18 Begin_Ship_Placing Message by MessageParser
		Format: 
			type:report;status:18;
		"""
		msg = MessageParser().encode("report",{"status": "18"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string			
		#print ("type"+msg.split("type",1)[1])								
							
		self.assertTrue(msg == "type:report;status:18;")

	def test_beginShipPlacingDecoding(self):
		"""
		Checks the Decoding of 18 Begin_Ship_Placing Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:18;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"18")	
	
	#19 Game_Aborted
	def test_gameAbortedEncoding(self):
		"""	
		Checks the Encoding of 19 Gama_Aborted Message by MessageParser
		Format: 
			type:report;status:19;
		"""
		msg = MessageParser().encode("report",{"status": "19"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
		self.assertTrue(msg == "type:report;status:19;")

	def test_gameAbortedDecoding(self):
		"""	
		Checks the Decoding of 19 Gama_Aborted Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:19;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"19")
	#----------------------------------------------------------------------------	
	#2x Messages
	#---------------------------------------------------------------------------
	# 21 Successful_Move
	def test_successfulMoveEncoding(self):
		"""	
		Checks the Encoding of 21 Successful_Move Message by MessageParser
		Format: 
			type:report;status:21;
		"""
		msg = MessageParser().encode("report",{"status": "21"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:21;")

	def test_successfulMoveDecoding(self):
		"""	
		Checks the Decoding of 21 Successful_Move Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:21;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"21")

	# 22 Successful_Attack
	def test_successfulAttackEncoding(self):
		"""	
		Checks the Encoding of 22 Successful_Attack Message by MessageParser
		Format: 
			type:report;status:22;
		"""
		msg = MessageParser().encode("report",{"status": "22"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:22;")

	def test_successfulAttackDecoding(self):
		"""	
		Checks the Decoding of 22 Successful_Attack Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:22;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"22")
	
	# 23 Surrender_Accepted
	def test_surrenderAcceptedEncoding(self):
		"""	
		Checks the Encoding of 23 Surrender_Accepted Message by MessageParser
		Format: 
			type:report;status:23;
		"""
		msg = MessageParser().encode("report",{"status": "23"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:23;")

	def test_surrenderAcceptedDecoding(self):
		"""	
		Checks the Decoding of 23 Surrender_Accepted Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:23;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"23")

	# 24 Successful_Special_Attack
	def test_successfulSpecialAttackEncoding(self):
		"""
		Checks the Encoding of 24 Successful_Special_Attack Message by MessageParser
		Format: 
			type:report;status:24;
		"""
		msg = MessageParser().encode("report",{"status": "24"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:24;")

	def test_successfulSpecialAttackDecoding(self):
		"""
		Checks the Decoding of 24 Successful_Special_Attack Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:24;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"24")

	# 27 Successful_Game_Join
	def test_successfulGameJoinEncoding(self):
		"""
		Checks the Encoding of 27 Successful_Game_Join Message by MessageParser
		Format: 
			type:report;status:27;
		"""
		msg = MessageParser().encode("report",{"status": "27"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:27;")

	def test_successfulGameJoinDecoding(self):
		"""
		Checks the Decoding of 27 Successful_Game_Join Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:27;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"27")

	# 28 Successful_Game_Create
	def test_successfulGameCreateEncoding(self):
		"""
		Checks the Encoding of 28 Successful_Game_Create Message by MessageParser
		Format: 
			type:report;status:28;
		"""
		msg = MessageParser().encode("report",{"status": "28"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:28;")

	def test_successfulGameCreateDecoding(self):
		"""
		Checks the Decoding of 28 Successful_Game_Create Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:28;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"28")

	# 29 Successful_Ship_Placement
	def test_successfulShipPlacementEncoding(self):
		"""
		Checks the Encoding of 29 Successful_Ship_Placement Message by MessageParser
		Format: 
			type:report;status:29;
		"""
		msg = MessageParser().encode("report",{"status": "29"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:29;")

	def test_successfulShipPlacementDecoding(self):
		"""
		Checks the Decoding of 29 Successful_Ship_Placement Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:29;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"29")
	#----------------------------------------------------------------------------	
	#3x Messages
	#---------------------------------------------------------------------------
	#31 Illegal_Move
	def test_illegalMoveEncoding(self):
		"""
		Checks the Encoding of 31 Illegal_Move Message by MessageParser
		Format: 
			type:report;status:31;
		"""
		msg = MessageParser().encode("report",{"status": "31"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:31;")

	def test_illegalMoveDecoding(self):
		"""
		Checks the Decoding of 31 Illegal_Move Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:31;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"31")

	#32 Illegal_Special_Attack	
	def test_illegalSpecialAttackEncoding(self):
		"""
		Checks the Encoding of 32 Illegal_Special_Attack Message by MessageParser
		Format: 
			type:report;status:32;
		"""
		msg = MessageParser().encode("report",{"status": "32"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:32;")

	def test_illegalSpecialAttackDecoding(self):
		"""
		Checks the Decoding of 32 Illegal_Special_Attack Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:32;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"32")
	
	#33 Illegal_Field	
	def test_illegalFieldEncoding(self):
		"""
		Checks the Encoding of 33 Illegal_Field Message by MessageParser
		Format: 
			type:report;status:33;
		"""
		msg = MessageParser().encode("report",{"status": "33"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:33;")

	def test_illegalFieldDecoding(self):
		"""
		Checks the Decoding of 33 Illegal_Field Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:33;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"33")

	#34 Illegal_Ship_Index	
	def test_illegalShipIndexEncoding(self):
		"""
		Checks the Encoding of 34 Illegal_Ship_Index Message by MessageParser
		Format: 
			type:report;status:34;
		"""
		msg = MessageParser().encode("report",{"status": "34"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:34;")

	def test_illegalShipIndexDecoding(self):
		"""
		Checks the Decoding of 34 Illegal_Ship_Index Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:34;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"34")

	#37 Illegal_Game_Definition	
	def test_illegalGameDefinitionEncoding(self):
		"""
		Checks the Encoding of 37 Illegal_Game_Definition Message by MessageParser
		Format: 
			type:report;status:37;
		"""
		msg = MessageParser().encode("report",{"status": "37"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:37;")

	def test_illegalGameDefinitionDecoding(self):
		"""
		Checks the Decoding of 37 Illegal_Game_Definition Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:37;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"37")
	
	#38 Illegal_Ship_Placement	
	def test_illegalShipPlacementEncoding(self):
		"""
		Checks the Encoding of 38 Illegal_Ship_Placement Message by MessageParser
		Format:
			 type:report;status:38;
		"""
		msg = MessageParser().encode("report",{"status": "38"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:38;")

	def test_illegalShipPlacementDecoding(self):
		"""
		Checks the Decoding of 38 Illegal_Ship_Placement Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:38;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"38")
	
	#39 Illegal_Attack
	def test_illegalAttackEncoding(self):
		"""
		Checks the Encoding of 39 Illegal_Attack Message by MessageParser
		Format: 
			type:report;status:39;
		"""
		msg = MessageParser().encode("report",{"status": "39"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:39;")

	def test_illegalAttackDecoding(self):
		"""
		Checks the Decoding of 39 Illegal_Attack Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:39;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"39")
	#----------------------------------------------------------------------------	
	#4x Messages
	#---------------------------------------------------------------------------
	#40 Message_Not_Recognized	
	def test_messageNotRecongnizedEncoding(self):
		"""
		Checks the Encoding of 40 Message_Not_Recognized Message by MessageParser
		Format: 
			type:report;status:40;
		"""
		msg = MessageParser().encode("report",{"status": "40"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:40;")

	def test_messageNotRecongnizedDecoding(self):
		"""
		Checks the Decoding of 40 Message_Not_Recognized Message by MessageParser
		"""		
		messageType, params = MessageParser().decode("type:report;status:40;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"40")	
	
	#41 Not_Your_Turn	
	def test_notYourTurnEncoding(self):
		"""
		Checks the Encoding of 41 Not_Your_Turn Message by MessageParser
		Format: 
			type:report;status:41;
		"""
		msg = MessageParser().encode("report",{"status": "41"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:41;")

	def test_notYourTurnDecoding(self):
		"""
		Checks the Decoding of 41 Not_Your_Turn Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:report;status:41;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"41")
		
	#43 Not_In_Any_Game
	def test_notInAnyGameEncoding(self):
		"""
		Checks the Encoding of 43 Not_In_Any_Game Message by MessageParser
		Format: 
			type:report;status:43;
		"""
		msg = MessageParser().encode("report",{"status": "43"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:43;")

	def test_notInAnyGameDecoding(self):
		"""
		Checks the Decoding of 43 Not_In_Any_Game Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:43;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"43")
	
	#47 Game_Join_Denied	
	def test_gameJoinDeniedEncoding(self):
		"""
		Checks the Encoding of 47 Game_Join_Denied Message by MessageParser
		Format: 
			type:report;status:47;
		"""
		msg = MessageParser().encode("report",{"status": "47"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:47;")

	def test_gameJoinDeniedDecoding(self):
		"""
		Checks the Decoding of 47 Game_Join_Denied Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:47;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"47")
	
	#48 Game_Preparation_Ended	
	def test_gamePreparationEndedEncoding(self):
		"""
		Checks the Encoding of 48 Game_Preparation_Ended Message by MessageParser
		Format: 
			type:report;status:48;
		"""
		msg = MessageParser().encode("report",{"status": "48"})						
		msg=msg[2:].decode('utf-8') # decode it from bytes to string								
						
		self.assertTrue(msg == "type:report;status:48;")

	def test_gamePreparationEndedDecoding(self):
		"""
		Checks the Decoding of 48 Game_Preparation_Ended Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:report;status:48;")

		self.assertEqual(messageType, "report")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["status"],"48")
	
	
		
	###Client-Messages###
	#----------------------------------------------------------------------------------------	
	#Lobby Related Messages
	#----------------------------------------------------------------------------------------
	#nickname_set
	def test_nickNameSetEncoding(self):
		"""
		Checks the Encoding of nickname_set Message by MessageParser
		Format: 
			type:nickname_set;name:[nickname];
		"""
		msg = MessageParser().encode("nickname_set",{"name": "Dari"})				
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
		self.assertTrue(msg == "type:nickname_set;name:Dari;")

	def test_nickNameSetDecoding(self):
		"""
		Checks the Decoding of nickname_set Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:nickname_set;name:Dari;")

		self.assertEqual(messageType, "nickname_set")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"Dari")	
	
	#game_create
	def test_gameCreateEncoding(self):
		"""
		Checks the Encoding of game_create Message by MessageParser
		Format: 
			type:game_create;name:[name];
		"""
		msg = MessageParser().encode("game_create",{"name": "FCB"})				
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
		self.assertTrue(msg == "type:game_create;name:FCB;")

	def test_gameCreateDecoding(self):
		"""
		Checks the Decoding of game_create Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:game_create;name:FCB;")

		self.assertEqual(messageType, "game_create")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"FCB")
	
	#game_join	
	def test_gameJoinEncoding(self):
		"""
		Checks the Encoding of game_join Message by MessageParser
		Format: 
			type:game_join;name:[name];
		"""
		msg = MessageParser().encode("game_join",{"name": "FCB"})				
		msg=msg[2:].decode('utf-8') # decode it from bytes to string						
						
		self.assertTrue(msg == "type:game_join;name:FCB;")

	def test_gameJoinDecoding(self):
		"""
		Checks the Decoding of game_join Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:game_join;name:FCB;")

		self.assertEqual(messageType, "game_join")
		self.assertEqual(len(params), 1)
		self.assertEqual(params["name"],"FCB")

	#game_abort
	def test_gameAbortEncoding(self):
		"""
		Checks the Encoding of game_abort Message by MessageParser
		Format: 
			type:game_abort;
		"""
		msg = MessageParser().encode("game_abort",{})				
		msg=msg[2:].decode('utf-8') # decode it from bytes to string				
					
		self.assertTrue(msg == "type:game_abort;")

	def test_gameAbortDecoding(self):
		"""
		Checks the Encoding of game_abort Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:game_abort;")

		self.assertEqual(messageType, "game_abort")
		self.assertEqual(len(params), 0)
	
				
	#-----------------------------------------------------------------------------------------------------------------------	
	#Game-Related Messages
	#-----------------------------------------------------------------------------------------------------------------------	
	#board_init	
	def test_boardInitEncoding(self):
		"""
		Checks the Encoding of board_init Message by MessageParser
		Format: 
			type:board_init; ship_0_x:[number];ship_0_y:[number];ship_0_direction: [W|E|S|N];...;
			ship_9_x:[number];ship_9_y:[number];ship_9_direction: [W|E|S|N];
		"""
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
				
		#print (msg)
		# order of parameters is not deterministic
		check=True							
		for key,value in params.items():
			if((key+":"+value) not in msg): check=False
		if(check): self.assertTrue(True)		
		else: self.assertTrue(False)			

	def test_boardInitDecoding(self):
		"""
		Checks the Decoding of board_init Message by MessageParser
		"""
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
	def test_surrenderEncoding(self):
		"""
		Checks the Encoding of surrender Message by MessageParser
		Format: 
			type:surrender; 
		"""
		msg = MessageParser().encode("surrender",{})		
		msg=msg[2:].decode('utf-8') # decode it from bytes to string		
		
						
		self.assertTrue(msg == "type:surrender;")

	def test_surrenderDecoding(self):
		"""
		Checks the Decoding of surrender Message by MessageParser 
		"""
		messageType, params = MessageParser().decode("type:surrender;")

		self.assertEqual(messageType, "surrender")
		self.assertEqual(len(params), 0)
		
	#move
	def test_moveEncoding(self):
		"""
		Checks the Encoding of move Message by MessageParser
		Format:
			 type:move; ship_id:[id];direction:[W|E|S|N]; 
		"""
		msg = MessageParser().encode("move", {"ship_id": "5", "direction": "W"})		
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
				
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:move;direction:W;ship_id:5;" or
				msg== "type:move;ship_id:5;direction:W;")

	def test_moveDecoding(self):
		"""
		Checks the Decoding of move Message by MessageParser 
		"""		
		messageType, params = MessageParser().decode("type:move; ship_id:5; direction:W;")

		self.assertEqual(messageType, "move")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["ship_id"], "5")		# integers are strings at this step
		self.assertEqual(params["direction"], "W")	

	#attack
	def test_attackEncoding(self):
		"""
		Checks the Encoding of attack Message by MessageParser
		Format:
			 type:attack;coordinate_x:[number];coordinate_y:[number];
		"""
		msg = MessageParser().encode("attack", {"coordinate_x": "5", "coordinate_y": "14"})
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
		
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:attack;coordinate_y:14;coordinate_x:5;" or
				msg== "type:attack;coordinate_x:5;coordinate_y:14;")

	def test_attackDecoding(self):
		"""
		Checks the Decoding of attack Message by MessageParser
		"""
		messageType, params = MessageParser().decode("type:attack; coordinate_x:5; coordinate_y:14;")

		self.assertEqual(messageType, "attack")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["coordinate_x"], "5")		# integers are strings at this step
		self.assertEqual(params["coordinate_y"], "14")
	
	# special_attack 
	def test_attackSpecialEncoding(self):
		"""
		Checks the Encoding of special_attack Message by MessageParser
		Format: 
			type:special_attack;coordinate_x:[number];coordinate_y:[number];
		"""
		msg = MessageParser().encode("special_attack", {"coordinate_x": "5", "coordinate_y": "14"})
		msg=msg[2:].decode('utf-8') # decode it from bytes to string
			
		
		# order of parameters is not deterministic				
		self.assertTrue(msg == "type:special_attack;coordinate_y:14;coordinate_x:5;" or
				msg== "type:special_attack;coordinate_x:5;coordinate_y:14;")

	def test_attackSpecialDecoding(self):
		"""
		Checks the Decoding of special_attack Message by MessageParser
		"""	
		messageType, params = MessageParser().decode("type:special_attack; coordinate_x:5; coordinate_y:14;")

		self.assertEqual(messageType, "special_attack")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["coordinate_x"], "5")		# integers are strings at this step
		self.assertEqual(params["coordinate_y"], "14")
	

if __name__ == "__main__":
	unittest.main()
