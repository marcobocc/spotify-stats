from app import app

HOSTNAME = 'localhost'
PORT = 8080

app.run(host=HOSTNAME, port=PORT, debug=True)