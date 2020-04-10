# Socket.IO Example

This repository contains an example to demonstrate the real time audio streaming functionality using socketIO. The program uses client's browser to access the mic. The audio is streamed to the remote flask server. As of now the server receives the stream and saves its overlapping chunks on disk in real time. These chunks can be passed to machine learning models to get real time predictions on audio stream.

## How to Run

First create a virtual environment and import the requirements.

To start the server, run:

```
(venv) $ export FLASK_APP=socketio_examples.py
(venv) $ flask run
```

Finally, open _http://localhost:5000_ on your web browser to access the
application.

Toggle the mic icon to start and stop recording.
NOTE: Please record an audio of atleast 7 seconds for the results to show up.
