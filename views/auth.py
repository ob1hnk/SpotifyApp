import urllib.parse
import requests

from flask import Blueprint, redirect, request, session, jsonify
from datetime import datetime

CLIENT_ID = 'f26a393e04c54022a1128fa57934bb28'
CLIENT_SECRET = '548c06749f01495284bb312f3b735cbb'
REDIRECT_URI = 'http://172.31.20.187:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
        scope = 'user-read-private user-read-email user-read-currently-playing user-modify-playback-state'

        params = {
                'client_id': CLIENT_ID,
                'response_type': 'code',
                'scope': scope,
                'redirect_uri': REDIRECT_URI,
                'show_dialog': True
        }

        # instead of using requests lib 
        auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

        return redirect(auth_url)


@auth.route('/callback')
def callback():
        if 'error' in request.args:
                return jsonify({"error": request.args['error']})
        
        # if login was successful, query gives back code which we need to use to get access token
        if 'code' in request.args:
                req_body = {
                        'code': request.args['code'],
                        'grant_type': 'authorization_code',
                        'redirect_uri': REDIRECT_URI,
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET
                }

        # exchange authorization with access token
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/get_currently_playing')


@auth.route('/refresh-token')
def refresh_token():
        if 'refresh_token' not in session:
                return redirect('/login')
        
        if datetime.now().timestamp() > session['expires_at']:
                req_body = {
                        'grant_type': 'refresh_token',
                        'refresh_token': session['refresh_token'],
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET
                }

        response = request.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/get_currently_playing')