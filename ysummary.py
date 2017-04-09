from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('ysummary', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class Channel:
    def __init__(self, name, channelUrl, videos):
        self.name = name
        self.channelUrl = channelUrl
        self.videos = videos

class Video:
    def __init__(self, title, videoUrl, thumbnail, thumbAltText):
        self.title = title
        self.videoUrl = videoUrl
        self.thumbnail = thumbnail
        self.thumbAltText = thumbAltText


@app.route('/home.html')
def home():
    videos1 = [Video("Cats", "", "https://i.ytimg.com/vi/rHgCTRB3hfU/maxresdefault.jpg", "Alt Text")]
    videos2 = [Video("Animu Girls", "", "https://i.ytimg.com/vi/rHgCTRB3hfU/maxresdefault.jpg", "Jesse Cox Alt Text")]
    videos3 = [Video("Baking", "", "", "")]
    return render_template('home.html', 
        channels=[
        Channel("Seananners", "https://www.youtube.com/user/SeaNanners/videos", videos1), 
        Channel("Jesse Cox", "https://www.youtube.com/user/OMFGcata/videos", videos2),
        Channel("Cupquake", "http://www.colgate.com/en/us/oc/", videos3)])



if __name__ == '__main__':
    app.run(debug=True)