class MessageParser:
	"""
	Commonly used parser to encode and decode communication messages.
	"""

	def encode(self, type, params):
		"""
		Encodes a message.

		Args:
			type - the type of the message
			params - a map of parameters that will be encoding separately

		Returns:
			The exadecimal encoded message size and the message itself as a utf-8 string
		"""
		
		result = "type:%s;" % (type)
		for param, value in params.iteritems():
			result = "%s%s:%s;" % (result, param, value)

		return hex(len(result)), result

	def decode(self, message):
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
