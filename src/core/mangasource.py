import logging

logger = logging.getLogger()

from mangapi.helpers	import Util
from mangapi.core		import Manga
from mangapi.helpers	import HttpSessionPool

from lxml				import html

pool = HttpSessionPool.Instance()

class Source():
	#@Util.profiler
	def __init__(self, series_dict, manga_dict, chapter_dict):
		all_mangaseries_page_tree = html.fromstring(pool.session.get(series_dict['url_root'] + series_dict['url_manga_list'], stream = True, timeout = (2,10)).content)

		self.__series = {}

		from mangapi.helpers import HttpSessionPool
		from mangapi.helpers import MangaCache

		logger.debug('Initializing Cache Instance for Manga.')
		cache = MangaCache.Instance()

		for node in all_mangaseries_page_tree.xpath(series_dict['xpath_manga_list']):
			name = node.xpath('a/text()')[0].strip()
			url = node.xpath('a/@href')[0]
			if not cache.exists(url):
				cache.store(key = url, value = Manga(name, series_dict['url_root'] + url, manga_dict, chapter_dict))
			self.__series[name] = cache.retrieve(url)

	@property
	#@Util.profiler
	def series(self):
		return self.__series

	#@Util.profiler
	def __str__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'

	#@Util.profiler
	def __repr__(self):
		return self.__class__.__name__ + ': (' + ', '.join("%s: %s" % item for item in vars(self).items()) + ')'

class MangaFox(Source):
	def __init__(self):
		super().__init__(
			series_dict = {
				'url_root':			 'http://mangafox.me', 
				'url_manga_list':	   '/manga/',
				'xpath_manga_list':	 '//div[@class="mangalist"]/ul/li',
			},
			manga_dict = {
				'xpath_cover_url':	  '//div[@id="mangaimg"]/img/@src',
				'xpath_manga_props':	'//div[@id="mangaproperties"]/table/tbody/tr/td[2]/',
				'xpath_chapter_list':   '//div[@id="chapterlist"]/table[@id="listing"]'
			}
		)

class MangaHere(Source):
	def __init__(self):
		super().__init__(
			series_dict = {
				'url_root':			 'http://www.mangahere.co', 
				'url_manga_list':	   '/mangalist/',
				'xpath_manga_list':	 '//ul[@class="series_alpha"]//li',
			},
			manga_dict = {
				'xpath_cover_url':	  '//div[@id="mangaimg"]/img/@src',
				'xpath_manga_props':	'//div[@id="mangaproperties"]/table/tbody/tr/td:2/',
				'xpath_chapter_list':   '//div[@id="chapterlist"]/table[@id="listing"]'
			}
		)

class MangaPanda(Source):
	#@Util.profiler
	def __init__(self):
		super().__init__(
			series_dict = {
				'url_root':			'http://www.mangapanda.com', 
				'url_manga_list':	'/alphabetical',
				'xpath_manga_list':	'//ul[@class="series_alpha"]//li'
			},
			manga_dict = {
				'url_root':					'http://www.mangapanda.com',
				'xpath_cover_url':			'//div[@id="mangaimg"]/img/@src',
				'xpath_alt_name':			'//div[@id="mangaproperties"]/table/tr[2]/td[2]/text()',
				'xpath_release_year':		'//div[@id="mangaproperties"]/table/tr[3]/td[2]/text()',
				'xpath_status':				'//div[@id="mangaproperties"]/table/tr[4]/td[2]/text()',
				'xpath_author':				'//div[@id="mangaproperties"]/table/tr[5]/td[2]/text()',
				'xpath_artist':				'//div[@id="mangaproperties"]/table/tr[6]/td[2]/text()',
				'xpath_reading_direction':	'//div[@id="mangaproperties"]/table/tr[7]/td[2]/text()',
				'xpath_genres':				'//div[@id="mangaproperties"]/table/tr[8]/td[2]/a/span[@class="genretags"]/text()',
				'xpath_chapter_list':		'//div[@id="chapterlist"]/table[@id="listing"]/tr/td/a',
			},
			chapter_dict = {
				'url_root':				'http://www.mangapanda.com',
				'xpath_manga_page':		'//div[@id="imgholder"]/a/img[@id="img"]/@src',
				'xpath_max_pages':		'//div[@id="navi"]/div[@id="selectpage"]/text()'
			}
		)


class MangaReader(Source):
	def __init__(self):
		super().__init__(
			series_dict = {
				'url_root':			'http://www.mangareader.com', 
				'url_manga_list':	'/alphabetical',
				'xpath_manga_list':	'//ul[@class="series_alpha"]//li'
			},
			manga_dict = {
				'url_root':					'http://www.mangareader.com',
				'xpath_cover_url':			'//div[@id="mangaimg"]/img/@src',
				'xpath_alt_name':			'//div[@id="mangaproperties"]/table/tr[2]/td[2]/text()',
				'xpath_release_year':		'//div[@id="mangaproperties"]/table/tr[3]/td[2]/text()',
				'xpath_status':				'//div[@id="mangaproperties"]/table/tr[4]/td[2]/text()',
				'xpath_author':				'//div[@id="mangaproperties"]/table/tr[5]/td[2]/text()',
				'xpath_artist':				'//div[@id="mangaproperties"]/table/tr[6]/td[2]/text()',
				'xpath_reading_direction':	'//div[@id="mangaproperties"]/table/tr[7]/td[2]/text()',
				'xpath_genres':				'//div[@id="mangaproperties"]/table/tr[8]/td[2]/a/span[@class="genretags"]/text()',
				'xpath_chapter_list':		'//div[@id="chapterlist"]/table[@id="listing"]/tr/td/a',
			},
			chapter_dict = {
				'url_root':				'http://www.mangareader.com',
				'xpath_manga_page':		'//div[@id="imgholder"]/a/img[@id="img"]/@src',
				'xpath_max_pages':		'//div[@id="navi"]/div[@id="selectpage"]/text()'
			}
		)

class MangaPark(Source):
	def __init__(self):
		super().__init__(
			series_dict = {
				'url_root':			'http://www.mangareader.com', 
				'url_manga_list':	'/alphabetical',
				'xpath_manga_list':	'//ul[@class="series_alpha"]//li'
			},
			manga_dict = {
				'url_root':					'http://www.mangareader.com',
				'xpath_cover_url':			'//div[@id="mangaimg"]/img/@src',
				'xpath_alt_name':			'//div[@id="mangaproperties"]/table/tr[2]/td[2]/text()',
				'xpath_release_year':		'//div[@id="mangaproperties"]/table/tr[3]/td[2]/text()',
				'xpath_status':				'//div[@id="mangaproperties"]/table/tr[4]/td[2]/text()',
				'xpath_author':				'//div[@id="mangaproperties"]/table/tr[5]/td[2]/text()',
				'xpath_artist':				'//div[@id="mangaproperties"]/table/tr[6]/td[2]/text()',
				'xpath_reading_direction':	'//div[@id="mangaproperties"]/table/tr[7]/td[2]/text()',
				'xpath_genres':				'//div[@id="mangaproperties"]/table/tr[8]/td[2]/a/span[@class="genretags"]/text()',
				'xpath_chapter_list':		'//div[@id="chapterlist"]/table[@id="listing"]/tr/td/a',
			},
			chapter_dict = {
				'url_root':				'http://www.mangareader.com',
				'xpath_manga_page':		'//div[@id="imgholder"]/a/img[@id="img"]/@src',
				'xpath_max_pages':		'//div[@id="navi"]/div[@id="selectpage"]/text()'
			}
		)