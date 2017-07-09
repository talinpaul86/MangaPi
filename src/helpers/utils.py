class Singleton:
	"""
	A non-thread-safe helper class to ease implementing singletons.
	This should be used as a decorator -- not a metaclass -- to the
	class that should be a singleton.

	The decorated class can define one `__init__` function that
	takes only the `self` argument. Also, the decorated class cannot be
	inherited from. Other than that, there are no restrictions that apply
	to the decorated class.

	To get the singleton instance, use the `Instance` method. Trying
	to use `__call__` will result in a `TypeError` being raised.
	"""

	def __init__(self, decorated):
		self._decorated = decorated

	def Instance(self):
		"""
		Returns the singleton instance. Upon its first call, it creates a
		new instance of the decorated class and calls its `__init__` method.
		On all subsequent calls, the already created instance is returned.
		"""
		try:
			return self._instance
		except AttributeError:
			self._instance = self._decorated()
			return self._instance

	def __call__(self):
		raise TypeError('Singletons must be accessed through `Instance()`.')

	def __instancecheck__(self, inst):
		return isinstance(inst, self._decorated)


class Util():
	def __init__(self):
		pass

	@property
	def test_internet_connection(self, host="8.8.8.8", port=53, timeout=3):
		"""
		Host: 8.8.8.8 (google-public-dns-a.google.com)
		OpenPort: 53/tcp
		Service: domain (DNS/TCP)
		"""
		import socket
		try:
			socket.setdefaulttimeout(timeout)
			socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
			return True
		except Exception as ex:
			logger.warn('Not connected to the Internet. Continuing in Offline-Mode.')
			return False

	def singleton(self, cls):
		''' Use class as singleton. '''
		import functools

		cls.__new_original__ = cls.__new__

		@functools.wraps(cls.__new__)
		def singleton_new(cls, *args, **kw):
			it =  cls.__dict__.get('__it__')
			if it is not None:
				return it

			cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
			it.__init_original__(*args, **kw)
			return it

		cls.__new__ = singleton_new
		cls.__init_original__ = cls.__init__
		cls.__init__ = object.__init__

		return cls

	def profiler(func):
		import cProfile

		def profiled_func(*args, **kwargs):
			profile = cProfile.Profile()
			try:
				profile.enable()
				result = func(*args, **kwargs)
				profile.disable()
				return result
			finally:
				profile.print_stats()
		return profiled_func

	def timeit(f):
		import time
		def f_timer(*args, **kwargs):
			start = time.time()
			result = f(*args, **kwargs)
			end = time.time()
			print(f.__name__, 'took', end - start, 'time')
			return result
		return f_timer