import os
from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['FILEDIR'] = 'static/_files/'
socketio = SocketIO(app)

from audio import bp as audio_bp

app.register_blueprint(audio_bp, url_prefix='/audio')


@app.route('/')
def index():
    return render_template('index.html')
