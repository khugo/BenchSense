# bench_sense

Bench sense is a script for detecting when a person is sitting on a chair and
logging that data to Google Sheets. It requires a Raspberry Pi with a pressure
sensor hooked up to it in a very specific manner.

## Running

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
