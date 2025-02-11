import requests
import pickle
import sys

from tools import crawl_path, check_cutter


# This script attempts to uncover all relevant information from the individual wiki pages.


def get_abfluss(which="/wiki/Elz_(Rhein)"):
    wikiurl = "https://de.wikipedia.org" + which
    response = requests.get(wikiurl)
    # HTML formating not consistent. Sometimes we need the second split element
    cutter = check_cutter(response.text, which)
    for x in range(1, 6):
        try:
            q = response.text.split(cutter)[x]
            if "Abfluss&#160;über" in q:
                abfluss = q.split("Abfluss&#160;über")
                return (
                    abfluss[1]
                    .split("→")[0]
                    .split("<a href=")[1]
                    .split('" title="')[0][1:]
                )
            else:
                q = q.split("Mündung")[2].split('href="')
                for possible in q:
                    if "/wiki/" in possible:
                        proposal = possible.split(" title=")[0][:-1]
                        return proposal
                if x == 4:
                    print("No matching end point found: " + which)
        except:
            continue


def main():
    rivers = pickle.load(open(crawl_path + "river_names.p", "rb"))

    # 1. Go to each page and crawl the "Abfluss" river name or the sink node name (e.g. ocean)
    print("Loading Abfluss")
    saves = {}
    for x in rivers:
        try:
            q = get_abfluss(rivers[x])
            print(x + " success.")
        except:
            q = None
            print(x + " FAIL!")

        saves[x] = q

    # some corrections
    for x in saves:
        if not saves[x]:
            continue
        elif '&amp;action=edit&amp;redlink=1" class="new' in saves[x]:
            saves[x] = "/wiki/" + saves[x].split("?title=")[1].split("&amp;")[0]
        elif 'class="mw-redirect' in saves[x]:
            saves[x] = saves[x].replace('class="mw-redirect', "")

    # Double checks:
    print(len([x for x in saves if not saves[x]]))  # check for None
    pickle.dump(saves, open(crawl_path + "abfluss_saves_raw.p", "wb"))


if __name__ == "__main__":
    main()
