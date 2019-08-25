import asyncio
import gspread_asyncio
import datetime
from oauth2client.service_account import ServiceAccountCredentials

import config
from logger import logger


async def start_session():
    logger.info("Writing session start event")
    now = datetime.datetime.now()
    await insert_row(now, "start")


async def end_session():
    logger.info("Writing session stop event")
    now = datetime.datetime.now()
    await insert_row(now, "stop")


async def make_client():
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    return agc


async def insert_row(date, event):
    agc = await make_client()
    logger.info(f"Opening spreadsheet {config.GOOGLE_SHEETS_URL}")
    sheet = await agc.open_by_url(config.GOOGLE_SHEETS_URL)
    ws = await sheet.get_worksheet(0)
    date_str = date.strftime("%d/%m/%Y %H:%M:%S")
    logger.info(f"Inserting row [{date_str}, {event}]")
    await ws.insert_row([date_str, event])


def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
      ["https://spreadsheets.google.com/feeds",
      "https://www.googleapis.com/auth/spreadsheets"])
