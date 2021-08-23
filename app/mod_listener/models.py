from app import db

class Base(db.Model):
    __abstract__  = True

class Track(Base):
    __tablename__ = 'tracks'

    track_id = db.Column(db.String(128), nullable=False, primary_key=True)
    track_name = db.Column(db.String(128), nullable=False)
    artist_name = db.Column(db.String(128), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)

    def __init__(self, track_id, track_name, artist_name, duration_ms):
        self.track_id = track_id
        self.track_name = track_name
        self.artist_name = artist_name
        self.duration_ms = duration_ms

    def __repr__(self):
        return '<Track {id}>'.format(id=self.track_id)

class TrackStatistics(Base):
    __tablename__ = "tracks_statistics"

    track_id = db.Column(db.String(128), nullable=False, primary_key=True)
    play_count = db.Column(db.Integer, nullable=False)
    listening_secs = db.Column(db.Integer, nullable=False)
    max_uninterrupted_secs = db.Column(db.Integer, nullable=False)

    def __init__(self, track_id, play_count, listening_secs, max_uninterrupted_secs):
        self.track_id = track_id
        self.play_count = play_count
        self.listening_secs = listening_secs
        self.max_uninterrupted_secs = max_uninterrupted_secs

    def __repr__(self):
        return '<TrackStatistics {id}>'.format(id=self.track_id)

class PlaybackStream(Base):
    __tablename__ = 'playback_streams'

    timestamp = db.Column(db.Integer, nullable=False, primary_key=True)
    track_id = db.Column(db.String(128), nullable=False)
    progress_ms = db.Column(db.Integer,  nullable=False)
    listening_ms = db.Column(db.Integer,  nullable=False)
    elapsed_ms = db.Column(db.Integer,  nullable=False)

    def __init__(self, timestamp, track_id, progress_ms, elapsed_ms, listening_ms):
        self.timestamp = timestamp
        self.track_id = track_id
        self.progress_ms = progress_ms
        self.elapsed_ms = elapsed_ms
        self.listening_ms = listening_ms

    def __repr__(self):
        return '<PlaybackStream {timestamp}>'.format(timestamp=self.timestamp)