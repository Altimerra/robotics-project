from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
from threading import Thread, Event
from queue import Queue

message_queue = Queue()
shutdown_event = Event()

app = Flask(__name__)
def flask_worker():
    app.run(debug=True, use_reloader=False)


# Set up GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.OUT)  # Replace 17 with the GPIO pin you are using

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    command = request.form['command']

    if command == 'forward':
        #GPIO.output(17, GPIO.HIGH)
        message_queue.put("control,forward")

    elif command == 'backward':
        #GPIO.output(17, GPIO.LOW)
        message_queue.put("control,backward")

    elif command == 'left':
        #GPIO.output(17, GPIO.LOW)
        message_queue.put("control,left")

    elif command == 'right':
        #GPIO.output(17, GPIO.LOW)
        message_queue.put("control,right")

    return 'OK'

@app.route('/mode', methods=['POST'])
def mode():
    data = request.get_json()
    is_on = data.get('isOn', False)

    # Add your logic to handle the control signals based on the 'is_on' value
    if is_on:
        # Code to execute when the button is turned ON
        message_queue.put("mode,auto")
    else:
        # Code to execute when the button is turned OFF
        message_queue.put("mode,remote")

    # Send a response back to the client
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)