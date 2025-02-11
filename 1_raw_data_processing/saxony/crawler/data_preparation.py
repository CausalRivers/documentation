import pandas as pd
import functools as ft
import numpy as np
from pathlib import Path
import utm
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        "Tool to format manual downloaded pegelonline data from Saxony.")

    parser.add_argument("--raw_path", type=str,
                        default="raw_responses",
                        help="path to raw files!")
    
    parser.add_argument("--stammdaten", type=str,
                        default="../Stammdaten_Hochwasser.csv",
                        help="path to the stammdaten containing river information!")

    parser.add_argument("--output_path", default="./processed",
                        help="Data save path")

    return parser.parse_args()


def process_data(args):
    meta = pd.read_csv(args.stammdaten)
    raw_list = list(Path(args.raw_path).glob("*.csv"))

    holder = []
    for raw in raw_list:
        data = pd.read_csv(raw)
        if "Q" not in data.columns: 
            print(f"Found no discharge in {raw}")
        else:
            stack = data[["Q_timestamp", "Q"]].dropna()
            stack["Q_timestamp"] = pd.to_datetime(stack["Q_timestamp"].str[:-9])
            stack.drop_duplicates("Q_timestamp", inplace=True)
            stack.rename(columns={"Q":raw.stem.split("_")[-2]}, inplace=True)
            stack.index = stack["Q_timestamp"]
            stack.drop(columns="Q_timestamp", inplace=True)
            holder.append(stack)

    df_final = ft.reduce(lambda left, right: pd.merge(left, right,how="outer", left_index=True, right_index=True), holder)
    df_final.index.name = "datetime"
    df_final.columns = [x + "_s" for x in df_final.columns]

    meta_data_saxony = meta.loc[
        meta["Pegelkennziffer"].isin(np.array([x[:-2] for x in df_final.columns]).astype(int)),
        [
            "Pegelkennziffer",
            "Pegelname",
            "Gewaesser",
            "Ostwert",
            "Nordwert",
            "Lage am Wasserlauf (km)",
            "Pegelnullpunkt (m)",
            "Gebietskennzahl"
        ],
    ]

    # saxony parsing
    for ind, line in meta_data_saxony.iterrows():
        try:
            meta_data_saxony.loc[ind, ["Ostwert", "Nordwert"]] = utm.to_latlon(
                line["Ostwert"], line["Nordwert"], 33, "U"
            )
        except Exception as e:
            print(e)


    meta_data_saxony.index = meta_data_saxony["Pegelkennziffer"].values
    meta_data_saxony = meta_data_saxony[["Gewaesser",	"Ostwert",	"Nordwert",	"Lage am Wasserlauf (km)",	"Pegelnullpunkt (m)"]]
    meta_data_saxony.columns = ["R", "X", "Y", "D", "H"]
    meta_data_saxony.index.name = "ID"


    meta_data_saxony["QD"] = -1
    meta_data_saxony["QH"] = -1
    meta_data_saxony["QX"] = -1
    meta_data_saxony["QY"] = -1
    meta_data_saxony["QR"] = -1

    meta_data_saxony.loc[~(meta_data_saxony["X"].isnull()), "QX"] = 0
    meta_data_saxony.loc[~(meta_data_saxony["Y"].isnull()), "QY"] = 0
    meta_data_saxony.loc[~(meta_data_saxony["D"].isnull()), "QD"] = 0
    meta_data_saxony.loc[~(meta_data_saxony["R"].isnull()), "QR"] = 0
    meta_data_saxony.loc[~(meta_data_saxony["H"].isnull()), "QH"] = 0

    outdir = Path(args.output_path)
    outdir.mkdir(parents=True, exist_ok=True)

    meta_data_saxony.to_csv(outdir / "saxony_flood_meta_data.csv")
    df_final.to_csv(outdir / "saxony_flood_processed.csv")

    print("\nYou will find the final data and metadata under:")
    print(outdir / "saxony_flood_processed.csv")
    print(outdir / "saxony_flood_meta_data.csv")
    


if __name__ == "__main__":
    args = get_args()
    process_data(args)
