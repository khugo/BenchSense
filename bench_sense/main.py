from sensor import sense, cleanup
import asyncio

from logger import logger
from tracking import start_session, end_session


async def main():
    logger.info("Starting to sense the bench")
    await sense(start_session, end_session)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info("Interrupted, exiting")
finally:
    cleanup()
