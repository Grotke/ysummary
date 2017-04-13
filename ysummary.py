from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
import YoutubeDataFetcher


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('ysummary', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class Channel:
    def __init__(self, name, channelId, videos):
        self.name = name
        if channelId:
            self.channelUrl = "https://www.youtube.com/channel/"+channelId
        else:
            self.channelUrl = ""
        self.videos = videos

class Video:
    def __init__(self, title, videoId, thumbnail, thumbAltText):
        self.title = title
        if videoId:
            self.videoUrl = "https://www.youtube.com/watch?v=" + videoId
        else:
            self.videoUrl = ""
        self.thumbnail = thumbnail
        self.thumbAltText = thumbAltText


@app.route('/')
def home():
    uploadPlaylistIds = ["UUq54nlcoX-0pLcN5RhxHyug", "UUqg2eLFNUu3QN3dttNeOWkw", "UUCbfB3cQtkEAiKfdRQnfQvw"]
    youtube = YoutubeDataFetcher.YoutubeDataFetcher()
    channels = youtube.fetchVideos(uploadPlaylistIds)
    return render_template('home.html', 
        channels=channels)



if __name__ == '__main__':
    app.run(debug=True)