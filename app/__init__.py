from flask import Flask, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

'''
    config.json
    ---------------------------------------------------------------
    {
        "BASE_DIR" : "",
        "SQLALCHEMY_DATABASE_URI" : "",
        "DEBUG" : true,
        "CSRF_ENABLED" : true,
        "CSRF_SESSION_KEY" : "xxxxxxxxxxxxxxxx",
        "SECRET_KEY" : "xxxxxxxxxxxxxxxx",
        "SPOTIFY_CLIENT_ID" : "xxxxxxxxxxxxxxxx",
        "SPOTIFY_CLIENT_SECRET" : "xxxxxxxxxxxxxxxx",
        "SPOTIFY_REDIRECT_URI" : "http://<HOSTNAME>/auth/create_session/"
    }
'''
app.config.from_json('config.json')
app.config['BASE_DIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASE_DIR'], 'app.db')

db = SQLAlchemy(app)

from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_listener.controllers import mod_listener as listener_module

app.register_blueprint(auth_module)
app.register_blueprint(listener_module)

db.create_all()
db.session.commit()

@app.route('/')
def index():
    if session.get('access_token'):
        return render_template('index.html')
    else:
        return redirect('/auth/signin/')
