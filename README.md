# bench_sense

Bench sense is a script for detecting when a person is sitting on a chair and
logging that data to Google Sheets. It requires a Raspberry Pi with a pressure
sensor hooked up to it in a very specific manner.

## Running

*To really use the script you first need to [configure](README.md#Configuration) the Google Sheets access.*

First install [Poetry](https://poetry.eustace.io), which is used for managing
the Python environment and dependencies.

Then install the dependencies

```sh
poetry install
```

Then start the script

``` sh
poetry run start
```

Bench sense is now listening for pressure on the sensor, and will report sitting
start and end times to the Google Sheet defined in `bench_sense/config.py`.

## Configuration

### Google Sheets

To run the script, you need API access to Google Drive and Google Sheets. Generate credentials to those and put the credentials JSON file that you got to the root of this folder with a file name of `credentials.json`.

Then you need to create a sheet and give access to that for the credentials you just created. Find the email from `credentials.json` and invite that email to edit the sheet from the normal sharing UI.
