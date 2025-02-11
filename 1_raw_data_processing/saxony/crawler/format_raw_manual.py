import argparse
from datetime import datetime, timedelta
import os

def get_args():
    parser = argparse.ArgumentParser(
        "Tool to format manual downloaded pegelonline data from Saxony.")

    parser.add_argument("--raw_path", type=str,
                        default="raw_manual/pegelonline.csv",
                        help="path to raw directory!")
    
    parser.add_argument("--stammdaten", type=str,
                        default="../Stammdaten_Hochwasser.csv",
                        help="path to the stammdaten containing river information!")

    parser.add_argument("--output_path", default="./raw_responses",
                        help="Data save path")

    return parser.parse_args()

def parse_day_header(header):
    header = header.replace('"', '').split(";")
    river = header[2].capitalize()
    pegel = header[3].capitalize()
    p_id = header[4]
    date = header[0]
    return date, river, pegel, p_id


def build_timestamp(date, time):
    date = datetime.strptime(date, '%d.%m.%Y').date()
    if time == "24:00":
        # fix mistake with 24 o clock
        time = "00:00"
        date = date + timedelta(days=1)

    date = str(date)
    timestamp = f"{date}T{time}:00+01:00"
    return timestamp


def parse_manual_pegelonline(args):
    with open(args.raw_path) as f:
        lines = f.readlines()
    
    lines = [line.replace('"', '').replace("\n", "").replace(",", ".") for line in lines]

    days = []

    day = []
    for line in lines:
        if len(line) == 0:
            # new day or different river
            days.append(day)
            day = []
        else:
            day.append(line)
    # add last day
    days.append(day)

    per_pegel = {}
    for day in days:
        date, river, pegel, p_id = parse_day_header(day[0])
        
        if pegel in per_pegel:
            pass
        else:
            per_pegel[pegel] = {
                "data" : ["Q,Q_timestamp\n"],
                "save_name": f"{pegel}_{river}_{p_id}_Ziel.csv"
            }

        day_data = day[1:]

        for data_row in day_data:
            time, Q = data_row.split(";")
            if Q.startswith("XXX"):
                continue
            per_pegel[pegel]["data"].append(f"{Q},{build_timestamp(date,time)}\n")

    return per_pegel


def save_pegel_data(args, pegel_data):
    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)


    for pegel in pegel_data:
        data = pegel_data[pegel]
        path = os.path.join(args.output_path, data["save_name"])
        with open(path, "w") as f:
            f.writelines(data["data"])
        print("finished: ", path)
    
    print("Completed reformating!")


if __name__ == "__main__":
    args = get_args()
    parsed_pegel_data = parse_manual_pegelonline(args)
    save_pegel_data(args, parsed_pegel_data)