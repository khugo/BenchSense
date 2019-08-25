import RPi.GPIO as GPIO
import time

INPUT_PIN = 4
SITTING_THRESHOLD = 100

def sense(on_sit_down, on_get_up):
    GPIO.setmode(GPIO.BCM)

    sitting_down = False
    while True:
        time = rc_time(INPUT_PIN)
        if time < SITTING_THRESHOLD:
            if sitting_down == False:
                on_sit_down()
            sitting_down = True
        else:
            if sitting_down == True:
                on_get_up()
            sitting_down = False

def cleanup():
    GPIO.cleanup()

def rc_time(pin_to_circuit):
    tick = 0

    #Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        tick += 1

    return tick
