import argparse
import pickle
from tools import get_elevation_of_point, crawl_path
import time

# This script attempts to uncover all relevant information from the individual wiki pages.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sink_nodes", action="store_true")
    args = parser.parse_args()

    if args.sink_nodes:
        rivers = pickle.load(open(crawl_path + "end_coordinates_sink_saves_raws.p", "rb"))
    else:
        rivers = pickle.load(open(crawl_path + "end_coordinates_saves_raw.p", "rb"))
    print("loading coords")
    # 4. Attempt to crawl the "raw coordinates available"

    timer = time.time()
    n_request = 1

    saves = {}
    for x in rivers:
        if not rivers[x]:
            saves[x] = None
            print(x + " FAIL!")
        else:
            print(n_request)
            # Handels the 500 requests per minute with some buffers
            if n_request % 490 == 0:
                wait = timer - time.time()
                if wait < 60:
                    time.sleep(60 - wait + 10)
                    timer = time.time()
                    n_request = 1
            try:
                q = get_elevation_of_point(rivers[x])
                n_request += 1

                print(x + " success.")
            except:
                q = None
                print(x + " FAIL!")
            saves[x] = q

    if args.sink_nodes:
        pickle.dump(saves, open(crawl_path + "height_sink_saves_raw.p", "wb"))
    else:
        pickle.dump(saves, open(crawl_path + "height_saves_raw.p", "wb"))
    print("Done.")


if __name__ == "__main__":
    main()
