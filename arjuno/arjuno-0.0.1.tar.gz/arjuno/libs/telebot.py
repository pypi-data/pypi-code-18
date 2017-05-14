from .lib_serial import *
from .lib_telegram import *

def main(port,baudrate):
	serial = Serializer(port=port,baudrate=baudrate)
	data = serial.recv()
	return data

def main_tele(port,baudrate):
	"""
	:input: dict
	command = [0]
	token = [1]
	chat_id = [2] optional
	message = [3] optional
	"""
	serial = Serializer(port=port,baudrate=baudrate)
	data = serial.recv()
	data = data.split("|")
	token = data[1]
	command = data[0]

	if len(data)>1:
		msg = data[2]
	else:
		msg = ""

	tele = TelegramBot(token=token)
	read_data = tele.read_message()
	read_telegram = read_data.split("|")
	chat_id = read_telegram[1]
	if command == "READ":
		return read_data
	elif command == "SEND":
		tele.send_message(msg,chat_id)
		return

def read(token):

	pass