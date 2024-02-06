import requests

from datetime import datetime
from flask import Blueprint, redirect, jsonify, session, render_template

API_BASE_URL = 'https://api.spotify.com/v1/'

currently_playing = Blueprint('currently_playing', __name__)

@currently_playing.route('/get_currently_playing')
def get_currently_playing():
        if 'access_token' not in session:
                return redirect('/login')
        if datetime.now().timestamp() > session['expires_at']:
                return redirect('/refresh-token')
        
        headers = {
                'Authorization': f"Bearer {session['access_token']}"
        }

        response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)

        if response.status_code == 200:
                currently_playing_data = response.json()
                return render_template('currently_playing.html', data=currently_playing_data)
        else:
                error_message = f"Failed to retrieve currently playing data. Status code: {response.status_code}"
                return render_template('error.html', error_message=error_message)
        
@currently_playing.route('/get_jsonified')
def get_jsonified():
        headers = {
                'Authorization': f"Bearer {session['access_token']}"
        }

        response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
        out = response.json()
        return jsonify(out)