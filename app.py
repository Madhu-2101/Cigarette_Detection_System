from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading
from database import fetch_removal_logs, fetch_current_counts  

app = Flask(__name__)
socketio = SocketIO(app)

detection_process = None  # To keep track of the detection process

def start_detection():
    """ Run the real_time_detection.py script in a subprocess """
    global detection_process
    # Start the detection process
    detection_process = subprocess.Popen(['venv/Scripts/python', 'real_time_detection.py'])

@app.route('/')
def index():
    """ Route for the main page, fetching logs from the database """
    logs = fetch_removal_logs()
    current_counts = fetch_current_counts()
    return render_template('index.html', logs=logs, current_counts=current_counts)



@socketio.on('start_video')
def handle_start_video():
    """ Handle the start video event from the frontend """
    # Start the detection process in a separate thread
    detection_thread = threading.Thread(target=start_detection)
    detection_thread.start()
    
    # Notify client that the video detection has started
    emit('video_started', {'message': 'Video detection started.'})

@socketio.on('stop_video')
def handle_stop_video():
    """ Handle the stop video event from the frontend """
    global detection_process
    if detection_process:
        detection_process.terminate()  # Terminate the subprocess
        detection_process = None  # Reset the detection process
        emit('video_stopped', {'message': 'Video detection stopped.'})


if __name__ == '__main__':
    socketio.run(app, debug=True)