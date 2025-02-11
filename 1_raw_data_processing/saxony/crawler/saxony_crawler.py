import argparse
import requests
import json
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
from build_xml_requests import build_soap_envelope, parse_response
from tqdm import tqdm


# https://www.pegelonline.wsv.de/gast/pegeltabelle/download?messgroesse_ids=1966,1969,1967,1968&parameter=8
# this link can be used to crawl the elbe data which is missing in the services


API_URL = "https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/webservices/spurwerte-ws?wsdl"
HEADER = {'content-type': 'application/soap+xml'}


def get_args():
    parser = argparse.ArgumentParser(
        "Tool to test crawl riverdata from Saxony.")

    parser.add_argument("--credentials", type=str,
                        default="ENTER_YOUR_CREDENTIALS.json",
                        help="path to json containing login credentials!")
    
    parser.add_argument("--stammdaten", type=str,
                        default="../Stammdaten.csv",
                        help="path to the stammdaten containing river information!")

    parser.add_argument("--resolution", type=str,
                        default="Ziel-MW-1T",
                        help="Ziel ... 15 minutes; \
                              Ziel-TW-1H ... 1 hour; \
                              Ziel-MW-1T ... 1 day")

    parser.add_argument("--start_date", type=str,
                        default=(date.today() - timedelta(weeks=4)
                                 ).strftime("%Y-%m-%d"),
                        help="format: YYYY-MM-DD, if none then defaults to 4 weeks ago.\
                         However, api allows only for last 5 years.")

    parser.add_argument("--end_date", type=str,
                        default=date.today().strftime("%Y-%m-%d"),
                        help="format: YYYY-MM-DD, defaults to today.")

    parser.add_argument("--debug", default=False, action="store_true",
                        help="Only run for one pegel.")

    parser.add_argument("--disable_cache", default=False, action="store_true",
                        help="disables raw responses cache.")

    parser.add_argument("--force_api_call", default=False, action="store_true",
                        help="If true, then cached responses are ignored!")
    parser.add_argument("--output_path", default="./raw_responses",
                        help="Data save path")

    return parser.parse_args()


def parse_str_to_date(str_date):
    """takes a string representation of a date
    (YYYY-MM-DD) and returns a datetime.date object.

    Args:
        str_date (str): date in YYYY-MM-DD
    """
    return date(*[int(x) for x in str_date.split("-")])


def load_credentials(path):
    """Reads credentials from given json file.

    Args:
        path (pathlike): patho to credentials .json
    """
    with open(args.credentials, "r") as f:
        credentials = json.load(f)
    return (credentials["username"], credentials["password"])


def get_datepairs_list(start, end):
    """Builds a list of 10 day intervals to iterate over."""
    datepairs = []
    while start < end:
        if start + timedelta(10) < end:
            datepairs.append((start, start+timedelta(10)))
        else:
            datepairs.append((start, end+timedelta(1)))

        start += timedelta(10)

    return datepairs


def load_stammdaten(path="Stammdaten.csv"):
    """Loads Stammdaten, i.e., list of measurement stations and metadata.

    Args:
        path (str, optional): path to "Stammdaten.csv".
    """
    return pd.read_csv(path)


def update_data_dict(data_dict, update):
    """takes a data dict and an update dict.
    Checks whether the keys of update dict are part of data dict.
    if yes:
        extend already existing data in dict
    if no:
        adds the data to dict

    Args:
        data_dict (dict): containing data that is tracked
        update (dict): containing updates
    """
    for quantity, value in update.items():
        if value:
            if quantity in data_dict:
                data_dict[quantity].extend(value)
            else:
                data_dict[quantity] = value


def clean_name(name):
    """Takes string and removes whitespaces"""
    return name.strip().replace(" ", "")


def patch_results(data_dict):
    """adds empty string rows for columns with less data."""
    if not data_dict:
        return
    maxlen = max([len(data_dict[x]) for x in data_dict])

    for key in data_dict:
        if len(data_dict[key]) < maxlen:
            data_dict[key].extend(
                ["" for _ in range(len(data_dict[key]), maxlen)])


def crawl_river_data(args):
    """Crawls the defined river data.

    Args:
        args (argparse args): command line arguments.
    """
    credentials = load_credentials(args.credentials)
    stammdf = load_stammdaten(args.stammdaten)
    end_date = parse_str_to_date(args.end_date)

    # iterate over all measurement stations
    for _, row in stammdf.iterrows():
        print(
            f"Querying river {row['Gewaesser']} data at {row['Pegelname']} station")

        # 1. check whether start date is given
        if not args.start_date:
            start_date = row["Durchfluss Q seit"]

            if not isinstance(start_date, str):
                # take date for waterheight if no discharge date is given
                start_date = row["Wasserstand W seit"]

            start_date = "-".join(start_date.split(".")[::-1])
            start_date = parse_str_to_date(start_date)
        else:
            start_date = parse_str_to_date(args.start_date)

        results_dict = {}
        # we now have a start and an end date for the current station
        # the api allows call with a maximum length of 240h -> 10 days
        # Hence, we have to iterate from start_date to end_date
        # in 10 day steps
        datepairs = get_datepairs_list(start_date, end_date)
        for sdate, edate in tqdm(datepairs):
            if not args.force_api_call:
                root = root = Path("./raw_responses")
                cached_response = root / \
                    f"{row['Pegelkennziffer']}_{args.resolution}_{sdate}_{edate}.xml"

                if cached_response.is_file():
                    with open(cached_response, "r") as f:
                        response = f.read()
                else:
                    response = None
            else:
                response = None

            if not response:
                xml_envelope = build_soap_envelope(row["Pegelkennziffer"],
                                                   str(sdate), str(edate),
                                                   args.resolution)

                response = requests.post(
                    API_URL, data=xml_envelope, headers=HEADER,
                    auth=credentials)

                response = response.content.decode('utf-8', errors='ignore')

                if not args.disable_cache:
                    root = Path("./raw_responses")
                    if not root.is_dir():
                        root.mkdir(parents=True, exist_ok=True)
                    with open(root /
                              f"{row['Pegelkennziffer']}_{args.resolution}_{sdate}_{edate}.xml",
                              "w") as f:
                        f.write(response)

            parsed_response = parse_response(response)
            update_data_dict(results_dict, parsed_response)

        patch_results(results_dict)
        ts_df = pd.DataFrame.from_dict(results_dict)
        save_root = Path(args.output_path)
        if not save_root.is_dir():
            save_root.mkdir(parents=True, exist_ok=True)

        save_file = save_root / \
            f"{clean_name(row['Pegelname'])}_{clean_name(row['Gewaesser'])}_{row['Pegelkennziffer']}_{args.resolution}.csv"

        if not ts_df.empty:
            ts_df.to_csv(save_file, index=False)
        else:
            print(
                f"Found no data for the specified dates:\n\
                      {args.start_date} to {args.end_date}.")

        if args.debug:
            break


if __name__ == "__main__":
    args = get_args()
    if args.resolution not in ["Ziel", "Ziel-TW-1H", "Ziel-MW-1T"]:
        raise ValueError(
            f"--resolution {args.resolution} is not valid -> use --help.")
    crawl_river_data(args)
