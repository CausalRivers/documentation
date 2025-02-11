from bs4 import BeautifulSoup
import requests
import pickle
from tools import crawl_path

# This script attempts to uncover all relevant information from the individual wiki pages.


def get_river_list():
    wikiurl = "https://de.wikipedia.org/wiki/Liste_von_Fl%C3%BCssen_in_Deutschland"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, "html.parser")
    indiatable = soup.find("table", {"class": "wikitable"})
    # split the raw text to get the list
    a = response.text.split(". Das Mündungsgewässer ist in Klammern angegeben.")[1]
    b = a.split("Anmerkungen")[0].split("\n")
    # extract the complete list of rivers and their corresponding wiki link
    rivers = {}
    for x in b[2:-1]:
        try:
            line = x.split(" –")
            line = line[1].split('"')
            rivers[line[3]] = line[1]
        except:
            print(x)
    del rivers["new"]
    rivers["Schiltach"] = "/wiki/Schiltach_(Fluss)"
    rivers["Rauda"] = "/wiki/Rauda_(Fluss)"
    return rivers


def get_river_list_from_category(x):

    stack = {}
    response = requests.get(x)
    rivers = (
        response.text.split(" insgesamt.")[1]
        .split('Special:CentralAutoLogin/start?type=1x1" alt=""')[0]
        .split("/wiki/")
    )
    for ritem in rivers[1:-1]:
        try:
            rlink = "/wiki/" + ritem.split(' title="')[0][:-1]
            name = ritem.split('" title="')[1].split('">')[0]
        except:
            print(ritem)
        stack[name] = rlink
    # some corrections:
    for x in stack:
        if '" class="mw-redirect' in stack[x]:
            # print("rewrite wiki url")
            stack[x] = stack[x].replace('" class="mw-redirect', "")
    return stack


def main():

    stack = []

    # 1. Crawl the big list of rivers from wiki including the links to the individual wiki pages.
    rivers = get_river_list()
    print("Base list", len(rivers))
    stack.append(rivers)
    # 2. Crawl the kategorie lists of the individual states.
    sources = [
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Th%C3%BCringen", "T"],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Th%C3%BCringen&pagefrom=Schleuse%0ASchleuse+%28Fluss%29#mw-pages",
            "T",
        ],
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Sachsen", "S"],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Sachsen&pagefrom=Lockwitzbach#mw-pages",
            "S",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Sachsen&pagefrom=Weissiger+Dorfbach%0AWei%C3%9Figer+Dorfbach#mw-pages",
            "S",
        ],
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Brandenburg", "BR"],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Brandenburg&pagefrom=Priorgraben#mw-pages",
            "BR",
        ],
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Berlin", "B"],
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Sachsen-Anhalt", "SA"],
        [
            "https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Mecklenburg-Vorpommern",
            "MV",
        ],
        ["https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Bayern", "BA"],
        # bayern is a lot
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Buchbach+Eger%0ABuchbach+%28Eger%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Fleutersbach#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Hammerbach+Isar%0AHammerbach+%28Kleine+Isar%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Klaffenbach+Isar%0AKlaffenbach+%28Isar%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Lohr%0ALohr+%28Fluss%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Pondorfbach#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Schippach+Erf%0ASchippach+%28Erf%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Sulzbach+Main%0ASulzbach+%28Main%29#mw-pages",
            "BA",
        ],
        [
            "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Bayern&pagefrom=Wolfsbronner+Muhlbach%0AWolfsbronner+M%C3%BChlbach#mw-pages",
            "BA",
        ],
    ]

    seperated_stack = {}
    for x in sources:
        rivers = get_river_list_from_category(x[0])
        if x[1] in seperated_stack.keys():
            seperated_stack[x[1]].append(rivers)
        else:
            seperated_stack[x[1]] = [rivers]
        print(x, len(rivers))
        stack.append(rivers)

    super_dict = {}
    for d in stack:
        for key in d.keys():
            if key in super_dict.keys():
                pass
            else:
                super_dict[key] = d[key]
    pickle.dump(super_dict, open(crawl_path + "river_names.p", "wb"))

    sep_dict = {}
    for listing in seperated_stack:
        joint_dict = {}
        for d in seperated_stack[listing]:
            for key in d.keys():
                if key in joint_dict.keys():
                    pass
                else:
                    joint_dict[key] = d[key]
        sep_dict[listing] = joint_dict
    pickle.dump(sep_dict, open(crawl_path + "seperated_river_names.p", "wb"))

    # same again for end points
    stack = []
    sources = [
        "https://de.wikipedia.org/wiki/Kategorie:Bucht_in_Mecklenburg-Vorpommern",
        "https://de.wikipedia.org/wiki/Kategorie:Bucht_in_Niedersachsen",
        "https://de.wikipedia.org/wiki/Kategorie:Bucht_in_Schleswig-Holstein",
        "https://de.wikipedia.org/wiki/Kategorie:Bucht_in_Hamburg",
        "https://de.wikipedia.org/wiki/Kategorie:K%C3%BCstengew%C3%A4sser_(Deutschland)",
        "https://de.wikipedia.org/wiki/Kategorie:Meerenge_(Ostsee)",
        "https://de.wikipedia.org/wiki/Kategorie:See_in_Schleswig-Holstein",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:See_in_Schleswig-Holstein&pagefrom=Ratzeburger+See#mw-pages",
        "https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Belgien",
        "https://de.wikipedia.org/wiki/Kategorie:See_in_Bayern",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:See_in_Bayern&pagefrom=Heimstettener+See#mw-pages",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:See_in_Bayern&pagefrom=Schleissbuhlweiher%0ASchlei%C3%9Fb%C3%BChlweiher#mw-pages",
        "https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Tschechien",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Tschechien&pagefrom=Kocovsky+potok%0AKo%C4%8Dovsk%C3%BD+potok#mw-pages",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Tschechien&pagefrom=Schwarze+Pockau#mw-pages",
        "https://de.wikipedia.org/wiki/Kategorie:Stausee_in_Bayern",
        "https://de.wikipedia.org/wiki/Kategorie:Fluss_in_Hessen",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Hessen&pagefrom=Formbach#mw-pages",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Hessen&pagefrom=Lauter+Wetter%0ALauter+%28Wetter%29#mw-pages",
        "https://de.wikipedia.org/w/index.php?title=Kategorie:Fluss_in_Hessen&pagefrom=Schwalm+Eder%0ASchwalm+%28Eder%29#mw-pages",
    ]
    for x in sources:
        rivers = get_river_list_from_category(x)
        print(x, len(rivers))
        stack.append(rivers)

    super_dict = {}
    for d in stack:
        for key in d.keys():
            if key in super_dict.keys():
                pass
            else:
                super_dict[key] = d[key]
    pickle.dump(super_dict, open(crawl_path + "/sink_names.p", "wb"))

    print("Done.")


if __name__ == "__main__":
    main()
