from apiclient.discovery import build
from apiclient.errors import HttpError
from ysummary import Video, Channel

class YoutubeDataFetcher:
	def __init__(self):
		self.DEVELOPER_KEY = "AIzaSyAd8QhFU3KJB33UIeFcITQtxZp-nkjplHc"
		self.YOUTUBE_API_SERVICE_NAME = "youtube"
		self.YOUTUBE_API_VERSION = "v3"
		self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)


	def connect(self):
		search_response = youtube.search().list(
    q="seananners",
    part="id,snippet",
    maxResults=5
  ).execute()

		return search_response

	def fetchVideos(self, playlistIds):
		channels = []
		for playId in playlistIds:
			searchResponse = self.youtube.playlistItems().list(
				part="id,snippet,contentDetails",
				maxResults=5,
				playlistId=playId
				).execute()

			rawItems = searchResponse.get("items")
			videoIds = []
			for rawItem in rawItems:
				videoIds.append(rawItem.get("contentDetails").get("videoId"))

			videos = []
			channelTitle = ""
			channelId = ""

			for videoId in videoIds:
				videoSearchResponse = self.youtube.videos().list(
					part="id,snippet,contentDetails",
					id=videoId
					).execute()
				snippet = videoSearchResponse.get("items")[0].get("snippet")
				channelTitle = snippet.get("channelTitle")
				channelId = snippet.get("channelId")
				videoTitle = snippet.get("title")
				thumbnail = snippet.get("thumbnails").get("default").get("url")
				thumbAltText = ""
				videos.append(Video(videoTitle, videoId, thumbnail, thumbAltText))
			channels.append(Channel(channelTitle, channelId, videos))
		return channels