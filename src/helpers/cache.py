import pickle

import requests
import gzip

from lxml	import html
from os		import path
from os		import stat
from io		import BytesIO

from .utils import Util

class Cache():
	#@Util.profiler
	def __init__(self, cache_file_name):
		self.__cache_file_name = cache_file_name
		self.__cache_updated_flag = False
		if path.isfile(self.__cache_file_name) and stat(self.__cache_file_name).st_size != 0:
			with gzip.GzipFile(self.__cache_file_name, 'rb') as f:
				self.__cache = pickle.load(f)
		else:
			self.__cache = {}

	#@Util.profiler
	def cache_updated_flag(self):
		return self.__cache_updated_flag

	#@Util.profiler
	def store(self, key, value):
		self.__cache[key] = value
		self.__cache_updated_flag = True

	#@Util.profiler
	def retrieve(self, key):
		return self.__cache[key]

	#@Util.profiler
	def save(self):
		if self.__cache_updated_flag:
			with gzip.GzipFile(self.__cache_file_name, 'wb') as file_ptr:
				pickle.dump(self.__cache, file_ptr, pickle.HIGHEST_PROTOCOL)

	#@Util.profiler
	def exists(self, key):
		return True if key in self.__cache else False


from .utils	import Singleton

@Singleton
class MangaCache(Cache):
	#@Util.profiler
	def __init__(self):
		super().__init__(cache_file_name = 'Manga.cache')

	#@Util.profiler
	def store(self, key, value):
		value.name
		value.url
		value.cover
		value.alt_names
		value.status
		value.release_year
		value.reading_direction
		value.author
		value.artist
		value.genres
		value.chapters
		super().store(key, value)

from .utils	import Singleton

@Singleton
class ChapterCache(Cache):
	#@Util.profiler
	def __init__(self):
		super().__init__(cache_file_name = 'Chapters.cache')