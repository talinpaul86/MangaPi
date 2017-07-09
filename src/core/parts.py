import logging

logger = logging.getLogger()

from lxml		import html
from io			import BytesIO

from .enums		import Genre
from .enums		import Status
from .enums		import ReadingDirection

from mangapi.helpers	import HttpSessionPool
from mangapi.helpers	import Util

'''
import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=64, pool_maxsize=128)
session.mount('http://', adapter)
session.headers.update({
	'Connection':'Keep-Alive',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
})
HttpSessionPool.Instance().session = session
'''

pool = HttpSessionPool.Instance()

class Manga():

	#@Util.profiler
	def __init__(self, name, url, manga_dict, chapter_dict):
		self.__name = name
		self.__url = url

		self.__xpath_chapter_list = manga_dict['xpath_chapter_list']
		self.__chapter_dict = chapter_dict

		manga_page_html_tree = html.fromstring(pool.session.get(url, stream = True, timeout = (2,10)).content)

		content = manga_page_html_tree.xpath(manga_dict['xpath_alt_name'])
		self.__alt_names = content[0].strip() if type(content) is list and content else ''

		self.__status = Status(manga_page_html_tree.xpath(manga_dict['xpath_status'])[0].strip())

		self.__reading_direction = ReadingDirection(manga_page_html_tree.xpath(manga_dict['xpath_reading_direction'])[0].strip())

		self.__genres = []
		for node in manga_page_html_tree.xpath(manga_dict['xpath_genres']):
			self.__genres.append(Genre(node))

		content = manga_page_html_tree.xpath(manga_dict['xpath_artist'])
		self.__artist = content[0].strip() if type(content) is list and content else ''

		content = manga_page_html_tree.xpath(manga_dict['xpath_author'])
		self.__author = content[0].strip() if type(content) is list and content else ''

		content = manga_page_html_tree.xpath(manga_dict['xpath_release_year'])
		self.__release_year = content[0].strip() if type(content) is list and content else ''

		self.__chapters = []

		self.__cover = BytesIO(pool.session.get(manga_page_html_tree.xpath(manga_dict['xpath_cover_url'])[0].strip(), stream = True).content)

	@property
	def name(self):
		return self.__name

	@property
	def url(self):
		return self.__url

	@property
	def cover(self):
		return self.__cover

	@property
	def alt_names(self):
		return self.__alt_names

	@property
	def status(self):
		return self.__status

	@property
	def release_year(self):
		return self.__release_year

	@property
	def reading_direction(self):
		return self.__reading_direction

	@property
	def author(self):
		return self.__author

	@property
	def artist(self):
		return self.__artist

	@property
	def genres(self):
		return self.__genres

	@property
	def chapters(self):
		if not self.__chapters:
			manga_page_html_tree = html.fromstring(pool.session.get(self.__url, stream = True, timeout = (2,10)).content)
			for node in manga_page_html_tree.xpath(self.__xpath_chapter_list):
				name	= node.xpath('text()')[0].strip()
				url		= self.__chapter_dict['url_root'] + node.xpath('@href')[0]
				self.__chapters.append(Chapter(name, url, self.__chapter_dict))
		return self.__chapters

	#@Util.profiler
	def __str__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'

	#@Util.profiler
	def __repr__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'


class Page():
	#@Util.profiler
	def __init__(self, url, image):
		self.__image = image
		self.__url = url

	@property
	def image(self):
		return self.__image

	@property
	def url(self):
		return self.__url

	#@Util.profiler
	def __str__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'

	#@Util.profiler
	def __repr__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'


class Chapter():
	#@Util.profiler
	def __init__(self, name, url, chapter_dict):
		self.__name = name
		self.__url = url
		self.__chapter_dict = chapter_dict

	@property
	def name(self):
		return self.__name

	@property
	def date_added(self):
		return self.__date_added

	@property
	def url(self):
		return self.__url

	@property
	def pages(self):
		if not self.__pages:
			from mangapi.helpers import ChapterCache

			logger.debug('Initializing Cache Instance for Chapters.')
			cache = ChapterCache.Instance()
			if not cache.exists(url):
				pages = []

				chapter_page_html_tree = html.fromstring(pool.session.get(url, stream = True, timeout = (2,10)).content)
				pages_max = chapter_page_html_tree.xpath(chapter_dict['xpath_max_pages'])[0].split(' ')[-1]
				for page in range(1, int(pages_max)):
					r = pool.session.get(url + '/' + str(page))
					manga_page_html_tree = html.fromstring(r.content)
					page_url = manga_page_html_tree.xpath(chapter_dict['xpath_manga_page'])[0]
					r = pool.session.get(page_url, stream = True)
					pages.append(Page(url = page_url, image = BytesIO(r.content)))
				cache.store(key = url, value = pages)

			self.__pages = cache.retrieve(key = url)
		return self.__pages

	#@Util.profiler
	def __str__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'

	#@Util.profiler
	def __repr__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'