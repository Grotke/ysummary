from apiclient.discovery import build
from apiclient.errors import HttpError
from ysummary import Video, Channel

class YoutubeDataFetcher:
	def __init__(self, httpAuth=''):
		self.DEVELOPER_KEY = "AIzaSyAd8QhFU3KJB33UIeFcITQtxZp-nkjplHc"
		self.YOUTUBE_API_SERVICE_NAME = "youtube"
		self.YOUTUBE_API_VERSION = "v3"
		self.httpAuth = httpAuth
		self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, http=self.httpAuth, developerKey=self.DEVELOPER_KEY)


	def connect(self):
		search_response = youtube.search().list(
    q="seananners",
    part="id,snippet",
    maxResults=5
  ).execute()

		return search_response

	def fetchVideosAndChannels(self, playlistIds):
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
				thumbnail = snippet.get("thumbnails").get("medium").get("url")
				thumbAltText = ""
				videos.append(Video(videoTitle, videoId, thumbnail, thumbAltText))
			channels.append(Channel(channelTitle, channelId, videos))
		return channels

	def fetchPlaylistIdsFromChannelIds(self, channelIds):
		uploadPlaylistIds = []
		for channelId in channelIds:
			uploadPlaylistIds.append(self.fetchPlaylistIdFromChannelId(channelId))
		return uploadPlaylistIds

	def fetchPlaylistIdFromChannelId(self, channelId):
		channelSearchResponse = self.youtube.channels().list(
			part="contentDetails",
			id=channelId
			).execute()

		channel = channelSearchResponse.get("items")[0]
		uploadPlaylistId = channel.get("contentDetails").get("relatedPlaylists").get("uploads")
		return uploadPlaylistId

	def fetchSubscribedChannelIds(self):
		subbedChannelIds = []
		if self.httpAuth:
			subSearchResponse = None
			nextPageToken = ''
			while not subSearchResponse or nextPageToken:
				subSearchResponse = self.youtube.subscriptions().list(
					part="snippet",
					mine="true",
					maxResults=5,
					pageToken=nextPageToken
				).execute()
				nextPageToken = subSearchResponse.get("nextPageToken")
				subs = subSearchResponse.get("items")
				for sub in subs:
					channelId = sub.get("snippet").get("resourceId").get("channelId")
					subbedChannelIds.append(channelId)

		
		return subbedChannelIds

	def fetchSubscriptions(self):
		channelIds = self.fetchSubscribedChannelIds()
		uploadPlaylistIds = self.fetchPlaylistIdsFromChannelIds(channelIds)
		return self.fetchVideosAndChannels(uploadPlaylistIds)







