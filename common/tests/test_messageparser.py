import sys
sys.path.append("..")

import unittest
from messageparser import *

class TestMessageParser(unittest.TestCase):

	def test_encoding(self):
		size, msg = MessageParser().encode("attack", {"coordinate_x": "5", "coordinate_y": "14"})

		self.assertEqual(size, "0x2b")
		self.assertEqual(msg, "type:attack;coordinate_y:14;coordinate_x:5;")

	def test_decoding(self):
		messageType, params = MessageParser().decode("2Dtype:attack; coordinate_x:5; coordinate_y:14;")

		self.assertEqual(messageType, "attack")
		self.assertEqual(len(params), 2)
		self.assertEqual(params["coordinate_x"], "5")		# integers are strings at this step
		self.assertEqual(params["coordinate_y"], "14")

if __name__ == "__main__":
	unittest.main()
