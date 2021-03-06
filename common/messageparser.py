import logging, struct
from helpers import *

class MessageParser:
	"""
	Commonly used parser to encode and decode communication messages.

	Author:
		Maximilian Hess <mail@maximilianhess.com>
	"""

	def encode(self, type, params):
		"""
		Encodes a message.

		Args:
			type: the type of the message
			params: a dictionary of parameters that will be encoded separately

		Returns:
			Returns the hexadecimal encoded message size and the message itself as a utf-8 string.
		"""

		result = "type:%s;" % type
		for param, value in params.items():
			result = "%s%s:%s;" % (result, param, value)

		return struct.pack('>H', len(result)) + b(result)

	def decode(self, message):
		"""
		Decodes a message.

		Args:
			message: a string representative of the message

		Returns:
			Returns the type of the message and the parameters as a dictionary.
		"""

		messageType = None
		params = {}
		tuples = message.split(";")
		for t in tuples:
			if t is not "":
				tokens = t.split(":")
				if tokens[0].strip() == "type":
					messageType = tokens[1].strip()
				else:
					try:
						params[tokens[0].strip()] = tokens[1].strip()
					except IndexError:
						params[tokens[0].strip()] = None

		return messageType, params
