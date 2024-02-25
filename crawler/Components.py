import RPi.GPIO as GPIO
import gpiozero
import time


def USonic(trig, echo):
    return gpiozero.DistanceSensor(echo=echo, trigger=trig)

class UltSonic:
    def __init__(self, trig, echo):
        self.TRIG = trig
        self.ECHO = echo

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def get_distance(self):
        # Trigger the ultrasonic sensor
        GPIO.output(self.TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, GPIO.LOW)

        # Measure the echo time
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        # Calculate the distance in centimeters
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance

class IRArray:
    def __init__(self, sensorpins):
        self.ir = [gpiozero.DigitalInputDevice(pin) for pin in sensorpins]


#class Drivetrain:
#    def __init__(self, l1, l2, r1, r2):
#        motorL = gpiozero.Motor(forward=l1, backward=l2)  # Motor 1
#        motorR = gpiozero.Motor(forward=r1, backward=r2)  # Motor 2

def Drivetrain(l1, l2, r1, r2):
    return gpiozero.Robot(
        left_motor= gpiozero.Motor(forward=l1, backward=l2), 
        right_motor= gpiozero.Motor(forward=r1, backward=r2),
    )
