import requests
import pickle
import sys
from tools import crawl_path

# This script attempts to uncover all relevant information from the individual wiki pages.




def get_river_id(which= "/wiki/Elz_(Rhein)"):
    wikiurl= "https://de.wikipedia.org" + which
    response=requests.get(wikiurl)
    if "Gew%C3%A4sserkennzahl" in response.text:
        q = response.text.split('Gew%C3%A4sserkennzahl')
        for x in range(1,3):
            try:
                return int(q[x].split("DE</a>:&#160;")[1].split("&")[0].split(",")[0])
            except:
                pass
    else:
        pass

def main():

    rivers = pickle.load(open(crawl_path + "river_names.p", "rb"))
    print("loading river ids")
    # 3. Attempt to crawl the "id" info
    saves = {}
    for x in rivers:
        try:
            q = get_river_id(rivers[x])
            print(x + " success.")
        except:
            q = None
            print(x + " FAIL!")
        saves[x] = q
    print([x for x in saves if not saves[x]])  # check for None
    pickle.dump(saves, open(crawl_path + "id_saves_raw.p", "wb"))
    print("Done.")


if __name__ == "__main__":
    main()
