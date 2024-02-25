import RPi.GPIO as GPIO
import time
from threading import Thread
from queue import Empty
 
import crawler.Components
from webapp.app import flask_worker, message_queue, shutdown_event

GPIO.setmode(GPIO.BCM)

flask_thread = Thread(target=flask_worker)

#us = crawler.Components.USonic(2,3)
#array = crawler.Components.IRArray({1,2,3,4,5,6,7,8})


if __name__ == '__main__':
    flask_thread.start()

    try:
        while not shutdown_event.is_set():
            try:
                message = message_queue.get(timeout=1)  # adjust timeout as needed
                # Process the message
                print(f"Received message: {message}")
            except Empty:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_event.set()
        flask_thread.join()
        GPIO.cleanup()