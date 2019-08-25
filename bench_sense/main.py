import asyncio

from bench_sense.sensor import sense, cleanup
from bench_sense.logger import logger
from bench_sense.tracking import start_session, end_session


def main():
    logger.info("Starting to sense the bench")
    try:
        asyncio.run(sense(start_session, end_session))
    except KeyboardInterrupt:
        logger.info("Interrupted, exiting")
    finally:
        cleanup()

if __name__ == '__main__' :
    main()
