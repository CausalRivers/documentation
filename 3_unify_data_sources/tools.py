import requests
import numpy as np

processed_path = ''
crawl_path = ''

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


def distance(c1, c2):
    # Conversion X, Y to km distance (considering curvature)
    deglen = 110.25
    x = c1[0] - c2[0]
    y = (c1[1] - c2[1])*np.cos(c1[0])
    return deglen*np.sqrt(x*x + y*y)

