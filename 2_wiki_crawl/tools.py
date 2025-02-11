import requests
crawl_path = "/home/datasets4/stein/rivers/crawl_saves_reproduce/"


def get_elevation_of_point(coords):
    # api-endpoint
    URL = "https://api.open-meteo.com/v1/elevation?"
    URL += "latitude="
    URL += str(coords[0])
    URL += "&"
    URL += "longitude="
    URL += str(coords[1])
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    # extracting data in json format
    data = r.json()
    return data["elevation"]


def check_cutter(text, which):
    # HTML formating not consistent. Sometimes we need the second split element
    if "Gew%C3%A4sserkennzahl" in text:
        return "Gew%C3%A4sserkennzahl"
    elif "Flusssystem" in text:
        return "Flusssystem"
    else:
        print("No cutter found: " + which)
        return False