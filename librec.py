from ppadb.client import Client as AdbClient


class AdbError(Exception):
	'Exception raised by adb errors'

	def __init__(self, message: str):
		self.message = f'ADB Exception: {message}'
		super(self, AdbError).__init__(self.message)


class ADB:
	HOST = "127.0.0.1"
	PORT = 5037
	CLIENT = None

	@classmethod
	def connect_server(cls, host: str=None, port: int=None):
		if host is None:
			host = cls.HOST
		else:
			cls.HOST = host
		if port is None:
			port = cls.PORT
		else:
			cls.PORT = port
		cls.CLIENT = AdbClient(host=cls.HOST, port=cls.PORT)

	@classmethod
	def check_server(cls):
		if cls.CLIENT is None:
			raise AdbError('CLIENT is None!')

	@classmethod
	def connect_device(cls, name: str):
		cls.check_server()
		return cls.CLIENT.deivce(name)

	@classmethod
	def list_devices(cls):
		cls.check_server()
		return cls.CLIENT.devices()

	@classmethod
	def kill(cls):
		self.check_server()
		cls.CLIENT.kill()

	@classmethod
	def killfoward_all(cls):
		self.check_server()
		cls.CLIENT.killfoward_all()

	@classmethod
	def list_forward(cls):
		self.check_server()
		return self.CLIENT.list_forward()

