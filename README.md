<p align="center"><img src="./docs/Spotify_Logo_RGB_Black.svg" width=200></p>

> <p style="text-align:justify;font-size:12px">⚠️ This project was created for personal uses and for learning. It might contain significant security vulnerabilities and should not be used in a production environment. Use at your own risk.</h6>

# Real-Time Spotify Tracker
<p style="text-align:justify;font-size:15px">The application collects information about the tracks that you listen to on Spotify and generates statistics about your listening habits in real-time. Some of the information currently recorded by the application include listening history, play counts and time of uninterrupted listening for each track. 
<br><br>
The application is written in Python. The back-end is implemented with Flask and SQLAlchemy, while the front-end is (at the moment) a HTML page running a JS script to fetch and update the playback stream in real-time.
</p>

## FAQ

#### 1. How is my listening activity tracked?

The application calls the Spotify Web API to access the details about the current state of your Spotify player. Such details (e.g., timestamp of your last action on the playback controls, track currently playing, track duration) are processed in real-time by the application to reconstruct the stream of your listening activities and to automatically generate statistics about the tracks you have played.

#### 2. How is an user authenticated?

The user is authenticated in accordance with [RFC-6749](https://datatracker.ietf.org/doc/html/rfc6749) (OAuth 2.0 authorization). The user is required to authenticate through the Spotify servers and must grant permission to access the details about playback controls, as specified by the authorization scope `user-read-playback-state`. If possible, the authorization is automatically refreshed by the application.

#### 3. Why is the user interface so minimal?

My main concern for this project was to experiment with the back-end. For this reason, I directed all of my efforts towards expanding the features and logic of the application. If, in the future, I decide I want to learn more about front-end development, I might pick up this project again to improve its user interface.

## How to set up

#### Setting up your Spotify application

1. Create your Spotify application from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) by following the instructions [here](https://developer.spotify.com/documentation/general/guides/app-settings/).

2. When instructed to add the redirect URI in your application settings, add `http:​//<HOSTNAME>/auth/create_session/` to the redirect URI whitelist. Replace *\<HOSTNAME>* with your web application's hostname (e.g., on the local machine you can use *localhost:8080* as hostname).

#### Creating the config.json file

1. In the app folder, create a file *config.json* and paste the following:
```
{ 
    "BASE_DIR" : "",  
    "SQLALCHEMY_DATABASE_URI" : "",  
    "DEBUG" : true,
    "CSRF_ENABLED" : true,
    "CSRF_SESSION_KEY" : "",
    "SECRET_KEY" : "",
    "SPOTIFY_CLIENT_ID" : "",
    "SPOTIFY_CLIENT_SECRET" : "",
    "SPOTIFY_REDIRECT_URI" : "http://<HOSTNAME>/auth/create_session/" 
}
```
2. Fill the *CSRF_SESSION_KEY* and *SECRET_KEY* fields with secret, unguessable values.

1. Copy the Client ID and the Client Secret from the application page in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) into the *SPOTIFY_CLIENT_ID* and *SPOTIFY_CLIENT_SECRET* fields, respectively.

1. Replace *\<HOSTNAME>* in the *SPOTIFY_REDIRECT_URI* field with your web application's hostname. This URI should coincide with the one previously added in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) in the steps above.

## How to use

1. Start the web application in your virtual environment with `python spotify-stats.py` (make sure you have installed all the required dependencies).

2. Connect from your browser to the *\<HOSTNAME>* specified during the setup phase.

3. If necessary, you will be redirected to the Spotify platform for authentication. Upon successful authentication, you will be redirected back to the original web page where your statistics will be recorded and displayed.




