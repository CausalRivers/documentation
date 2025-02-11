import argparse


import requests
import pickle
import sys

from tools import crawl_path

# This script attempts to uncover all relevant information from the individual wiki pages.


def get_end_coords(which="/wiki/Elz_(Rhein)"):
    wikiurl = "https://de.wikipedia.org" + which
    response = requests.get(wikiurl)
    body = response.text
    potential = body.split("Mündungshöhe")
    if len(potential) > 1:
        attempt = (
            potential[0]
            .split('href="https://geohack.toolforge.org/')[-1]
            .split(";params=")[1]
            .split("_N_")
        )
        N = attempt[0]
        E = attempt[1].split("_E_")[0]
        return N, E
    else:
        if "Mündung" in potential[0]:
            # first coodinate that comes after the first mentioning of mündung
            attempt = (
                potential[0]
                .split("Mündung")[2]
                .split('href="https://geohack.toolforge.org/')[1]
                .split(";params=")[1]
                .split("_N_")
            )
            N = attempt[0]
            E = attempt[1].split("_E_")[0]
            return N, E
        # Attempt single split

        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sink_nodes", action="store_true")
    args = parser.parse_args()

    if args.sink_nodes:
        rivers = pickle.load(open(crawl_path + "sink_names.p", "rb"))
    else:
        rivers = pickle.load(open(crawl_path + "river_names.p", "rb"))
    print("loading coords")
    # 4. Attempt to crawl the "raw coordinates available"
    saves = {}
    for x in rivers:
        try:
            q = get_end_coords(rivers[x])
            print(x + " success.")
        except:
            q = None
            print(x + " FAIL!")
        saves[x] = q

    print([x for x in saves if not saves[x]])  # check for None
    if args.sink_nodes:
        pickle.dump(saves, open(crawl_path + "end_coordinates_sink_saves_raw.p", "wb"))
    else:
        pickle.dump(saves, open(crawl_path + "end_coordinates_saves_raw.p", "wb"))
    print("Done.")


if __name__ == "__main__":
    main()
