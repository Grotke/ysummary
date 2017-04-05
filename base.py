from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('base', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class Channel:
    def __init__(self, name, videoUrl):
        self.name = name
        self.videoUrl = videoUrl


@app.route('/home.html')
def home():
    return render_template('home.html', 
        channels=[
        Channel("Seananners", "https://www.youtube.com/user/SeaNanners/videos"), 
        Channel("Jesse Cox", "https://www.youtube.com/user/OMFGcata/videos"),
        Channel("Cupquake", "http://www.colgate.com/en/us/oc/")])



if __name__ == '__main__':
    app.run(debug=True)