from flask import Blueprint, request, redirect, session, current_app
import requests
import urllib.parse

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # SPOTIFY_CSRF_TOKEN = ''
    qs = urllib.parse.urlencode({
        'client_id': current_app.config['SPOTIFY_CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': current_app.config['SPOTIFY_REDIRECT_URI'],
        # 'state': SPOTIFY_CSRF_TOKEN,
        'scope': 'user-read-playback-state'
    }, doseq=False)
    SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize/?'
    return redirect(SPOTIFY_AUTH_URL + qs)

@mod_auth.route('/create_session/')
def authorized():
    o = urllib.parse.urlparse(request.url)
    query = urllib.parse.parse_qs(o.query)
    if 'error' in query:
        return query['error'][0]
    elif 'code' in query:
        SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
        token_response = requests.post(SPOTIFY_TOKEN_URL, {
            'client_id': current_app.config['SPOTIFY_CLIENT_ID'],
            'client_secret': current_app.config['SPOTIFY_CLIENT_SECRET'],
            'redirect_uri': current_app.config['SPOTIFY_REDIRECT_URI'],
            'grant_type': 'authorization_code',
            'code': query['code'][0]
        })
        token_response_data = token_response.json()
        session['access_token'] = token_response_data['access_token']
        session['refresh_token'] = token_response_data['refresh_token']
        session['expires_in'] = token_response_data['expires_in']
        return redirect('/')

@mod_auth.route('/refresh_token/', methods=['GET', 'POST'])
def refresh_token():
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return redirect('/')
    SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    token_response = requests.post(SPOTIFY_TOKEN_URL, {
        'client_id' : current_app.config['SPOTIFY_CLIENT_ID'],
        'client_secret' : current_app.config['SPOTIFY_CLIENT_SECRET'],
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    })
    token_response_data = token_response.json()
    session['access_token'] = token_response_data['access_token']
    session['expires_in'] = token_response_data['expires_in']
    return redirect('/')