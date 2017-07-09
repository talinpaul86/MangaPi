from .utils import Singleton
from .utils import Util

@Singleton
class HttpSessionPool():
	def __init__(self):
		self.__session = None

	@property
	def session(self):
		return self.__session

	@session.setter
	def session(self, session):
		self.__session = session