class MessageParser:
	"""
	Commonly used parser to encode and decode communication messages.
	"""

	def encode(self, type, params):
		"""
		Encodes a message.

		Args:
			type - the type of the message
			params - a dictonary of parameters that will be encoded separately

		Returns:
			Returns the exadecimal encoded message size and the message itself as a utf-8 string.
		"""
		
		result = "type:%s;" % (type)
		for param, value in params.items():
			result = "%s%s:%s;" % (result, param, value)

		return ("%s" + result) % (str(hex(len(result)))[2:])

	def decode(self, message):
		"""
		Decodes a message.

		Args:
			message - a string representative of the message

		Returns:
			Returns the type of the message and the parameters as a dictonary.
		"""

		size = int(message[:2], 16)

		messageType = None
		params = {}
		tuples = message[2:].split(";")
		for t in tuples:
			if t is not "":
				tokens = t.split(":")
				if tokens[0].strip() == "type":
					messageType = tokens[1].strip()
				else:
					params[tokens[0].strip()] = tokens[1].strip()

		return messageType, params
