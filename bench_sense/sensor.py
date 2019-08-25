import RPi.GPIO as GPIO
import asyncio
import config

INPUT_PIN = 4
SITTING_THRESHOLD = 100

async def sense(on_sit_down, on_get_up):
    GPIO.setmode(GPIO.BCM)

    sitting_down = False
    while True:
        tick = 0

        # Output low on the pin
        GPIO.setup(INPUT_PIN, GPIO.OUT)
        GPIO.output(INPUT_PIN, GPIO.LOW)
        await asyncio.sleep(0.1)

        # Change the pin back to input
        GPIO.setup(INPUT_PIN, GPIO.IN)

        # Count until the pin goes high
        while (GPIO.input(INPUT_PIN) == GPIO.LOW):
            tick += 1
            await asyncio.sleep(0.01)
            # If it's been long enough since the pin has gone high, we are not sitting
            if tick >= config.GET_UP_WAIT_TIME_SECONDS * 100 and sitting_down:
                on_get_up()
                sitting_down = False
        # If it took short enough of a time for the pin to go high, we are applying enough pressure to count
        # as sitting
        if tick < SITTING_THRESHOLD and not sitting_down:
            on_sit_down()
            sitting_down = True


def cleanup():
    GPIO.cleanup()

