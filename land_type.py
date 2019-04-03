import numpy
import json
import requests

import multiprocessing as mp

OCEAN_MAP = []

def is_ocean(lat, long, session=requests.Session()):
    url = "http://api.geonames.org/oceanJSON"

    req_params = {
        'lat': lat,
        'lng': long,
        'username': "40i2"
    }

    r = session.get(url, params=req_params)
    ret = r.json()

    b = True if "ocean" in ret else False

    return b

def load_map():
    global OCEAN_MAP

    with open("ocean-coordinates", "r") as f:
        OCEAN_MAP = [ c.strip() for c in f.readlines()]


def is_ocean_local(lat, long):
    st = "{},{}".format(lat, long)
    if st in OCEAN_MAP:
        return True
    return False

if __name__ == "__main__":

    coords = []

    # NOT SO BAD
    # for lat in numpy.arange(41.131386, 41.208026, 0.0018):
    #     for lon in numpy.arange(-8.712680, -8.558663, 0.0025):

    for lat in numpy.arange(41.131386, 41.208026, 0.0015):
        for lon in numpy.arange(-8.712680, -8.558663, 0.0015):
            coords.append((lat, lon))

    session = requests.Session()

    #with open("data.json", "r") as f:
    #    data = json.load(f)

    data = {}

    # Step 1: Init multiprocessing.Pool()
    with open("ocean-coordinates", "a") as f:
        for lat, long in coords:
            st = "{},{}".format(lat, long)

            if st in data:
                print("Already know: ", st, " ", data[st])
            else:
                #b = pool.apply_async(is_ocean, args=(lat,lon,session))
                b = is_ocean(lat, long, session)
                data[st] = b
                print("Found", st, "-", b)

                if b:
                    f.write(st+"\n")
                    f.flush()


