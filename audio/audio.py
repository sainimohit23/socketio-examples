"""Audio Recording Socket.IO Example

Implements server-side audio recording.
"""
import os
import uuid
import wave
from flask import Blueprint, current_app, session, url_for, render_template
from flask_socketio import emit
from socketio_examples import socketio
# import pyaudio
import numpy as np

bp = Blueprint('audio', __name__, static_folder='static',
               template_folder='templates')

chunk_duration = 0.5 # Each read length in seconds from mic.
fs = 44100 # sampling rate for mic
chunk_samples = int(fs * chunk_duration) # Each read length in number of samples.

# Each model input data duration in seconds, need to be an integer numbers of chunk_duration
BASE_DIR = os.getcwd()
feed_duration = 10
feed_samples = int(fs * feed_duration)
data = 0
cnt = 0
channels=0
bps=0
flag=True
# def callback(in_data, frame_count, time_info, status):
#     global run, timeout, data, silence_threshold    
#     # if time.time() > timeout:
#     #     run = False        
#     data0 = np.frombuffer(in_data, dtype='int16')
#     # if np.abs(data0).mean() < silence_threshold:
#     #     sys.stdout.write('-')
#     #     return (in_data, pyaudio.paContinue)
#     # else:
#     #     sys.stdout.write('.')
#     data = np.append(data,data0)    
#     if len(data) > feed_samples:
#         data = data[-feed_samples:]
#         # Process data async by sending a queue.
#         q.put(data)
#     return (in_data, pyaudio.paContinue)


# def get_audio_input_stream(callback):
#     stream = pyaudio.PyAudio().open(
#         format=pyaudio.paInt16,
#         channels=1,
#         rate=fs,
#         input=True,
#         frames_per_buffer=chunk_samples,
#         input_device_index=0,
#         stream_callback=callback)
#     return stream


@bp.route('/')
def index():
    """Return the client application."""
    return render_template('audio/main.html')


@socketio.on('start-recording', namespace='/audio')
def start_recording(options):
    """Start recording audio from the client."""
    id = uuid.uuid4().hex  # server-side filename
    session['wavename'] = id + '.wav'
    # wf = wave.open(current_app.config['FILEDIR'] + session['wavename'], 'wb')
    # session['audiodata'] = np.zeros(feed_samples, dtype='int16')

    global fs, channels, bps
    session['audiobuffer'] = list()
    fs = options.get('fps', 44100)
    channels = options.get('numChannels', 1)
    bps = options.get('bps', 16) // 8
    print("sample rate: ", fs)

    files = os.listdir(os.path.join(BASE_DIR, "static/_files/"))
    for file in files:
        if file.endswith(".wav"):
            os.remove(os.path.join(BASE_DIR,'static/_files/', file))
    # session['wavefile'] = wf


@socketio.on('write-audio', namespace='/audio')
def write_audio(data):
    """Write a chunk of audio from the client."""
    # session['audiobuffer'] = np.append(session['audiobuffer'],data)
    global fs, cnt, channels, bps, flag
    session['audiobuffer'].append(data)
    if len(session['audiobuffer']) > 300:
        print("chunk completed ",len(session['audiobuffer']))
        wf = wave.open(current_app.config['FILEDIR'] + str(cnt) + session['wavename'], 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(bps)
        wf.setframerate(fs)
        for frame in session['audiobuffer'][:300]:
            wf.writeframes(frame)
        wf.close()
        session['audiobuffer'] = session['audiobuffer'][200:]
        cnt += 1

    # if len(session['audiobuffer']) == 500 and flag==True:
    #     for i in range(5):
    #         print("chunk completed ",len(session['audiobuffer']))
    #         wf = wave.open(current_app.config['FILEDIR'] + str(i) + session['wavename'], 'wb')
    #         wf.setnchannels(channels)
    #         wf.setsampwidth(bps)
    #         wf.setframerate(fs)
    #         for frame in session['audiobuffer'][:i*100]:
    #             wf.writeframes(frame)
    #         wf.close()
    #         # session['audiobuffer'] = session['audiobuffer'][300:]
    #     cnt += 1
    #     flag=False


@socketio.on('end-recording', namespace='/audio')
def end_recording():
    """Stop recording audio from the client."""
    # print("saving file")
    files = os.listdir(os.path.join(BASE_DIR, "static/_files/"))
    files.sort()
    print(files)
    for file in files:
        if file.endswith(".wav"):
            emit('add-wavefile', url_for('static', filename='_files/' + file))
    # session['wavefile'].close()
    del session['audiobuffer']
    del session['wavename']
