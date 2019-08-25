import asyncio

from bench_sense.sensor import sense, cleanup
from bench_sense.logger import logger
from bench_sense.tracking import start_session, end_session


async def main():
    logger.info("Starting to sense the bench")
    await sense(start_session, end_session)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info("Interrupted, exiting")
finally:
    cleanup()
