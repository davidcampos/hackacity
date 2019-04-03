import numpy
import json
import requests

def is_ocean(lat, long):
    url = "http://api.geonames.org/oceanJSON"

    req_params = {
        'lat': lat,
        'lng': long,
        'username': "40i2"
    }

    r = requests.get(url, params=req_params)
    ret = r.json()

    b = True if "ocean" in ret else False

    return b

if __name__ == "__main__":
    coords = []

    # NOT SO BAD
    # for lat in numpy.arange(41.131386, 41.208026, 0.0018):
    #     for lon in numpy.arange(-8.712680, -8.558663, 0.0025):

    for lat in numpy.arange(41.131386, 41.208026, 0.0015):
        for lon in numpy.arange(-8.712680, -8.558663, 0.0015):
            coords.append((lat, lon))

    #with open("data.json", "r") as f:
    #    data = json.load(f)

    data = {}

    for lat, long in coords:
        st = "{},{}".format(lat, long)

        if st in data:
            print("Already know: ", st, " ", data[st])
        else:
            url = "http://api.geonames.org/oceanJSON"

            req_params = {
                'lat': lat,
                'lng': long,
                'username': "40i2"
            }

            r = requests.get(url, params=req_params)
            ret = r.json()

            b = True if "ocean" in ret else False
            data[st] = b

            print("Found", st, "-", b)

    with open("data.json", "w") as f:
        json.dump(data,f)

