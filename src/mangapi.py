import logging
import atexit
import time, threading

from mangapi.helpers import MangaCache
from mangapi.helpers import ChapterCache

logger = logging.getLogger()

# create a file handler
handler = logging.FileHandler('./logs/MangaReader.log')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.DEBUG)

def exit_handler():
	logger.info('Updating cache before terminating.')
	MangaCache.Instance().save()
	ChapterCache.Instance().save()

atexit.register(exit_handler)


from mangapi.helpers	import HttpSessionPool

logger.debug('Initializing HttpSessionPool.')

'''
# Using python 3.4
from concurrent.futures import ProcessPoolExecutor
from requests import Session
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession

req_session = Session()
adapter = HTTPAdapter(pool_connections=64, pool_maxsize=128)
req_session.mount('http://', adapter)
req_session.headers.update({
	'Connection':'Keep-Alive',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
})
session = FuturesSession(executor = ProcessPoolExecutor(max_workers=2), session = req_session)
HttpSessionPool.Instance().session = session
'''

from requests import Session
from requests.adapters import HTTPAdapter

session = Session()
adapter = HTTPAdapter(pool_connections=64, pool_maxsize=128)
session.mount('http://', adapter)
session.headers.update({
	'Connection':'Keep-Alive',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
})
HttpSessionPool.Instance().session = session

class MangaPi():
	def __init__(self, sources):
		self.__sources = sources

	@property
	def sources(self):
		return self.__sources