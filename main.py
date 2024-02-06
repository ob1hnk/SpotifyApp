from flask import Flask, request, session
from views.auth import auth
from views.currently_playing import currently_playing

app = Flask(__name__)
app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

app.register_blueprint(auth)
app.register_blueprint(currently_playing)

@app.route('/')
def index():
        return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)