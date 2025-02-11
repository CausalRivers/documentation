# This script:
#
# 1. tests all data sources for consistency
# 2. prepares a 1 ts per node dataset
# 3. Exports data statistics for later usage.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import functools as ft
from os import listdir
import pickle
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default= "/home/datasets4/stein/rivers/processed/" )
    parser.add_argument('--filter_states', action="store_true")
    parser.add_argument('--nan_threshold', default=0.66, type=float)
    parser.add_argument('--states',default=("thuringia", "saxony", "mv", "brandenburg", "bscv", "berlin","saxony_anhalt"), type=str,nargs='+')
    args = parser.parse_args()


    # path where processed data is saved
    onlyfiles = [args.path + f for f in listdir(args.path) if "processed" in f]
    print("Found the following data files:")


    if args.filter_states:
        states = [args.path + x  + "_processed.csv" for x in args.states]
        onlyfiles  = [x for x in onlyfiles if x in states]
        print(onlyfiles)


    print("Loading...")
    ds = {}
    for x in onlyfiles:
        ds[x.split("/")[-1].split("processed.csv")[0]] = pd.read_csv(x, index_col=0)
    print(ds.keys())
    print(sum([len(ds[x].columns) for x in ds.keys()]))
    # check for duplicate ids. 


    # TS check (invalid timestamps)
    print("Double check dt stamps")
    # quickly transform dr
    for x in ds.keys():
        ds[x].index = pd.to_datetime(ds[x].index)
    # Map full dt to see if something is missing
    t = pd.to_datetime(
        np.arange(
            datetime(2019, 1, 1, 0, 0),
            datetime(2023, 12, 31, 23, 46),
            timedelta(minutes=15),
        ).astype(datetime)
    )


    # merge
    ds = ft.reduce(
        lambda left, right: pd.merge(
            left, right, left_index=True, right_index=True, how="outer"
        ),
        [ds[x] for x in ds.keys()],
    )
    ds = ds[~ds.index.duplicated(keep="first")]
    ds = ds[ds.index.year < 2024]
    print(len(ds.columns))

    print("Checking time stamp consistency....")

    # Double check for wacky timestamps.
    print([x for x in ds.index if x not in t])
    assert len([x for x in ds.index if x not in t]) == 0, "Wrong timestep"

    assert len([x for x in t if x not in ds.index]) == 0, "Msissing timestep"

    print("Checking data consistency....")

    empty = ds.isnull().sum() / len(ds)
    # make this flexible and the default should be what I have here.
    quite_possible_bricked = empty[empty >= args.nan_threshold].index

    print("Full Nan:")
    print("Ts with more than threshold percent data missing:")
    print(len(quite_possible_bricked))


    ds.drop(columns= ds[quite_possible_bricked].columns.values,inplace=True)
    print("Remain:")
    print(len(ds.columns))

    print("save full data.")
    ds.to_csv(args.path + "ts_ds.csv")

    pickle.dump(empty, open(args.path + "missing_stats.p", "wb"))
    # we save this also for quick usage later on.
    pickle.dump(quite_possible_bricked.values, open(args.path + "bricked_columns.p", "wb"))
    
    print("Saving bricked column names...")
    print("Done.")


if __name__ == "__main__":
    main()
