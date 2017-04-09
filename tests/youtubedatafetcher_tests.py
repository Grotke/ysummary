import YoutubeDataFetcher
import unittest

class YoutubeDataFetcherTestCase(unittest.TestCase):
	def setUp(self):
		self.fetcher = YoutubeDataFetcher.YoutubeDataFetcher()

	def test_connect(self):
		assert isinstance(self.fetcher.connect(), dict) is False


if __name__ == '__main__':
	unittest.main()