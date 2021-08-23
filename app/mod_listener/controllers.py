from flask import Blueprint, request, redirect, session, json
from app import db
from app.mod_listener.models import PlaybackStream, Track, TrackStatistics
import requests
import urllib.parse
from sqlalchemy import insert, func, desc
import math

mod_listener = Blueprint('listener', __name__, url_prefix='/listener')

def request_currently_playing(access_token):
    access_token = session.get('access_token')   
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer {token}'.format(token=access_token)
    }
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    if r.status_code != 200:
        error_data = {
            'error_code' : r.status_code,
            'reason' : r.reason
        }
        return error_data
    response_data = r.json()
    currently_playing = {
        'timestamp' : response_data['timestamp'],
        'progress_ms' : response_data['progress_ms'],
        'track_id' : response_data['item']['id'],
        'track_name' : response_data['item']['name'],
        'artist_name' : response_data['item']['artists'][0]['name'],
        'duration_ms' : response_data['item']['duration_ms']
    }
    return currently_playing

def update_current_stream(currently_playing):
    existing_stream = PlaybackStream.query.get(currently_playing['timestamp'])
    if existing_stream:
        # If there is already a stream with the current timestamp, update its information
        elapsed_time = currently_playing['progress_ms'] - existing_stream.progress_ms
        prev_listening_ms = existing_stream.listening_ms
        existing_stream.listening_ms = existing_stream.listening_ms + elapsed_time
        existing_stream.elapsed_ms = existing_stream.elapsed_ms + elapsed_time
        existing_stream.progress_ms = currently_playing['progress_ms']
        # Update the track statistics in real-time
        track_stats = TrackStatistics.query.get(currently_playing['track_id'])    
        if track_stats:
            track_stats.listening_secs = round(track_stats.listening_secs + elapsed_time / 1000) 
            track_stats.max_uninterrupted_secs = max(track_stats.max_uninterrupted_secs, round(existing_stream.listening_ms / 1000))
            MIN_LISTENING_PERCENTAGE = 20
            if prev_listening_ms < currently_playing['duration_ms'] * MIN_LISTENING_PERCENTAGE / 100 <= existing_stream.listening_ms:
                # A stream increases the play count only if it has lasted for more than MIN_LISTENING_PERCENTAGE % of the track duration
                track_stats.play_count = track_stats.play_count + 1
        return existing_stream
    else:
        TIME_WINDOW_MS = 30000
        last_stream = db.session.query(PlaybackStream).order_by(desc(PlaybackStream.timestamp)).first()
        might_match = True if last_stream and last_stream.track_id == currently_playing['track_id'] else False
        if might_match and currently_playing['timestamp'] - (last_stream.timestamp + last_stream.elapsed_ms) <= TIME_WINDOW_MS:
            # If there was already a stream of this track open and the user did not change track within TIME_WINDOW_MS milliseconds...
            # ...resume the previous stream
            last_stream.timestamp = currently_playing['timestamp']
            last_stream.progress_ms = currently_playing['progress_ms']
            last_stream.elapsed_ms = 0
            return last_stream
        else:
            # There is no available stream that can be resumed, create a new one
            new_stream = PlaybackStream(
                timestamp=currently_playing['timestamp'], 
                track_id=currently_playing['track_id'],
                progress_ms=currently_playing['progress_ms'],
                elapsed_ms=0,
                listening_ms=0)
            db.session.add(new_stream)
            # If it is the first time you are listening to this track, add it to the list of tracks...
            track = Track.query.get(currently_playing['track_id'])
            if not track:
                db.session.add(Track(
                    track_id=currently_playing['track_id'], 
                    track_name=currently_playing['track_name'],
                    artist_name=currently_playing['artist_name'],
                    duration_ms=currently_playing['duration_ms'],
                ))
            # ...and create a new record for collecting its statistics in real-time
            track_stats = TrackStatistics.query.get(currently_playing['track_id'])
            if not track_stats:
                db.session.add(TrackStatistics(
                    track_id=currently_playing['track_id'], 
                    play_count=0,
                    listening_secs=0,
                    max_uninterrupted_secs=0,
                ))
            return new_stream

@mod_listener.route('/update/', methods=['GET', 'POST'])
def listen():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')
    currently_playing = request_currently_playing(access_token)   
    error_code = currently_playing.get('error_code')
    if error_code:
        if error_code == 401:
            return redirect('/auth/refresh_token/')
        return (currently_playing.get('reason'), error_code)
    curr_stream = update_current_stream(currently_playing)
    track_stats = TrackStatistics.query.get(currently_playing['track_id'])
    db.session.commit()
    return json.dumps({
        'track_name' : currently_playing['track_name'],
        'artist_name' : currently_playing['artist_name'],
        'curr_listening_time' : round(curr_stream.listening_ms / 1000),
        'total_listening_time' : track_stats.listening_secs,
        'max_uninterrupted_secs' : track_stats.max_uninterrupted_secs,
        'play_count' : track_stats.play_count,
    })
