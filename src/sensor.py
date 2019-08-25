import RPi.GPIO as GPIO
import time
import asyncio

INPUT_PIN = 4
SITTING_THRESHOLD = 100


async def sense(on_sit_down, on_get_up):
    GPIO.setmode(GPIO.BCM)

    sitting_down = False
    while True:
        time = await rc_time(INPUT_PIN)
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


async def rc_time(pin_to_circuit):
    tick = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    await asyncio.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        print("Tick")
        tick += 1
        await asyncio.sleep(0.01)

    return tick
