import requests

from threading import Thread

class ArduinoConnect:
	def __init__(self, ip_addr, port_no):
		self.ip_addr = ip_addr
		self.port_no = port_no

	def call(self):
		try:
			Thread(target=requests.get, args=(self.ip_addr + '/?DETECT',)).start()
		except Exception as e:
			print(e)

# Example:
# ardConnect = ArduinoConnect('http://192.168.43.80', '80')
ardConnect = ArduinoConnect('', '')
