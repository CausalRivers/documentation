# Crawler for Saxony River Data

You need to make an account here: 
https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/portal/web/download-registrierung

Afterwards you have to put your login credentials into the corresponding .json.

## Usage

```
usage: Tool to test crawl riverdata from Saxony. [-h] [--credentials CREDENTIALS] [--resolution RESOLUTION] [--start_date START_DATE] [--end_date END_DATE] [--debug] [--disable_cache] [--force_api_call]

options:
  -h, --help            show this help message and exit
  --credentials CREDENTIALS
                        path to json containing login credentials!
  --resolution RESOLUTION
                        Ziel ... 15 minutes; Ziel-TW-1H ... 1 hour; Ziel-MW-1T ... 1 day
  --start_date START_DATE
                        format: YYYY-MM-DD, if none then defaults to 4 weeks ago. However, api allows only for last 5 years.
  --end_date END_DATE   format: YYYY-MM-DD, defaults to today.
  --debug               Only run for one pegel.
  --disable_cache       disables raw responses cache.
  --force_api_call      If true, then cached responses are ignored!
```

## Examples
Crawl from a specific start date:
```
python saxony_crawler.py --credentials <your credentials.json> --start_date 2021-07-01
```

Crawl between specific dates:
```
python saxony_crawler.py --credentials <your credentials.json> --start_date 2021-07-01 --end_date 2022-09-01
```

Crawl with 15 minutes resolution
```
python saxony_crawler.py --credentials <your credentials.json> --resolution Ziel
```