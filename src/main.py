from sensor import sense, cleanup
import asyncio


async def main():
    try:
        await sense(on_sit_down, on_get_up)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


def on_sit_down():
    print("Sit down")
    pass


last_session_start_time = None


def on_get_up():
    print("Stand down")
    pass
