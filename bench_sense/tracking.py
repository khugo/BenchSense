import asyncio
import gspread_asyncio
from gspread.exceptions import WorksheetNotFound
import arrow
from oauth2client.service_account import ServiceAccountCredentials

import bench_sense.config as config
from bench_sense.logger import logger

EVENT_TRACKING_WORKSHEET_NAME = "Events"
SESSION_TRACKING_WORKSHEET_NAME = "Sessions"


async def start_session():
    logger.info("Writing session start event")
    timestamp = arrow.now(config.TIMEZONE).timestamp
    spreadsheet = await get_spreadsheet()
    event_row = await get_latest_event(spreadsheet)
    if len(event_row) > 1 and event_row[1] == "start":
        logger.warning(
            "Expected last event to be 'stop' but it was 'start'. Starting a new session.")
    await insert_event(spreadsheet, timestamp, "start")


async def end_session():
    logger.info("Writing session stop event")
    end_timestamp = arrow.now(config.TIMEZONE).timestamp
    spreadsheet = await get_spreadsheet()
    latest_event_row = await get_latest_event(spreadsheet)

    if len(latest_event_row) < 2:
        logger.warning("Tried to end a session when it was not running")
        return

    if len(latest_event_row) > 1 and latest_event_row[1] == "stop":
        logger.warning(
            "Expected last event to be 'start' but it was 'stop'. Not ending the session.")
        return

    start_timestamp = int(latest_event_row[0])

    await insert_event(spreadsheet, end_timestamp, "stop")
    await insert_session(spreadsheet, start_timestamp, end_timestamp)


async def get_latest_event(spreadsheet):
    ws = await get_or_create_worksheet(spreadsheet, EVENT_TRACKING_WORKSHEET_NAME)
    return await ws.row_values(1)


async def get_or_create_worksheet(spreadsheet, worksheet_name):
    try:
        return await spreadsheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        return await spreadsheet.add_worksheet(worksheet_name, rows=10000, cols=10)


async def get_spreadsheet():
    logger.info(f"Opening spreadsheet {config.GOOGLE_SHEETS_URL}")
    agc = await make_client()
    sheet = await agc.open_by_url(config.GOOGLE_SHEETS_URL)
    return sheet


async def insert_event(spreadsheet, timestamp, event):
    ws = await get_or_create_worksheet(spreadsheet, EVENT_TRACKING_WORKSHEET_NAME)
    logger.info(f"Inserting event [{timestamp}, {event}]")
    await ws.insert_row([timestamp, event])


async def insert_session(spreadsheet, start_timestamp, end_timestamp):
    ws = await get_or_create_worksheet(spreadsheet, SESSION_TRACKING_WORKSHEET_NAME)
    start_date = arrow.get(start_timestamp).to(config.TIMEZONE)
    end_date = arrow.get(end_timestamp).to(config.TIMEZONE)
    duration_min = (end_date - start_date).seconds // 60
    start_date_str = start_date.format('DD/MM/YYYY HH:mm:ss')
    end_date_str = end_date.format('DD/MM/YYYY HH:mm:ss')

    logger.info(
        f"Inserting session [{start_date_str}, {end_date_str}, {duration_min}]")
    await ws.insert_row([start_date_str, end_date_str, duration_min])


async def make_client():
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    return agc


def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", [
            "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"])


def unix_timestamp(datetime):
    return time.mktime(datetime.timetuple())
