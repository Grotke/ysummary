from flask import Flask, render_template, redirect, url_for, request, session
from jinja2 import Environment, PackageLoader, select_autoescape
from oauth2client import client
import httplib2
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
    def __init__(self, title, videoId, thumbnail, thumbAltText, publishDate):
        self.title = title
        if videoId:
            self.videoUrl = "https://www.youtube.com/watch?v=" + videoId
        else:
            self.videoUrl = ""
        self.thumbnail = thumbnail
        self.thumbAltText = thumbAltText
        self.publishDate = publishDate


@app.route('/')
def home():
    loggedIn = False
    accessDenied = False
    channels = []
    if 'credentials' in session:
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        if credentials.access_token_expired:
            return redirect(url_for('auth'))
        loggedIn = True
        http_auth = credentials.authorize(httplib2.Http())
        uploadPlaylistIds = ["UUq54nlcoX-0pLcN5RhxHyug", "UUqg2eLFNUu3QN3dttNeOWkw", "UUCbfB3cQtkEAiKfdRQnfQvw"]
        youtube = YoutubeDataFetcher.YoutubeDataFetcher(httpAuth=http_auth)
        channels = youtube.fetchSubscriptions()
    if 'access_denied' in session:
        accessDenied = True
    return render_template('home.html', 
        channels=channels, loggedIn=loggedIn, accessDenied=accessDenied)

@app.route('/authorize')
def authorized():
    #if 'code' not in flask.request.args:
        #return redirect(url_for('trying'))
    return render_template('authorize.html')

@app.route('/auth')
def auth():
    session.clear()
    flow = client.flow_from_clientsecrets(
        '../client_secrets.json',
        scope="https://www.googleapis.com/auth/youtube.readonly",
        redirect_uri="http://127.0.0.1:5000" + url_for('auth'))
    #flow.params['include_granted_scopes']=True
    auth_uri = flow.step1_get_authorize_url()
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    elif 'error' in request.args:
        session['access_denied'] = request.args.get('error')
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('home'))


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4)
    app.run(debug=True)