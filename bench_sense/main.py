from sensor import sense, cleanup
import asyncio


async def main():
    print("Starting to sense the bench")
    try:
        await sense(on_sit_down, on_get_up)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


def on_sit_down():
    print("Sit down")


def on_get_up():
    print("Get up")

asyncio.run(main())
