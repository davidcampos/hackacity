import requests
import numpy
import csv

import json

import progressbar
from pprint import pprint

_DEFAULT_PARAMS = {
    'f': 'json',
    #'where': "1=1",  # 'where' clause is mandatory it takes a postgres-like query
    # 'where': "n_o > 10",                  # example where the number of reports event was over 10
    # 'where': "freguesia = 'Bonfim'",      # example for all the reports in 'Bonfim'
    # 'where': "ano > 2000",                # Caveat: For example in this dataset, this will not work as 'ano' is defined as "esriFieldTypeString"
    #'returnGeometry': 'true',
    #'outFields': '*',  # the fields that you want returned
    #'orderByFields': 'objectid ASC',
    # 'resultOffset': '4000',
    #'resultRecordCount': '10',  # for the purpose of the demonstration we are limiting to 10 results
    'geometryType': 'esriGeometryPoint',
    'geometry': '-8.629500540214053, 41.15801561717854',
    'inSR': '4326',
    'outSR': '4326',
    'returnIdsOnly': True
    # 'token': str(TOKEN)
}

def request_objects(geometry_object_str, mapNumber=77):
    req_params = _DEFAULT_PARAMS
    req_params['geometry'] = geometry_object_str

    url = 'https://servsig.cm-porto.pt/arcgis/rest/services/OpenData_APD/OpenData_APD/MapServer/{}/query'.format(mapNumber)
    r = requests.get(url, params=req_params)

    return r.json()


def request_objects_around_coordinate(lat,long, mapNumber=77):
    s = "{}, {}".format(long, lat)
    return request_objects(s, mapNumber)

def write_csv(category, dataList, t=None):
    if t is None:
        t = category

    fname = "POI_{}_{}.csv".format(category, t)
    with open(fname, 'w', newline='') as csvfile:
        fieldnames = ['type', 'lat', 'long', 'value', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for o in dataList:
            writer.writerow(o)

        print("Writen: ", fname)

if __name__ == "__main__":
    coords = []
    for lat in numpy.arange(41.131386,41.208026, 0.0018):
        for lon in numpy.arange(-8.712680,-8.558663, 0.0025):
            coords.append((lat,lon))

    print("N Cords: ", len(coords))

    ## Numbers
    ## Areas-verdes: {'map_number': 77, 'cat': 'GreenZone'}
    ## bairos: 43 {'map_number': 43,'cat': 'Bairos'}

    descr = {
        'map_number': 43,
        'cat': 'Bairos'
    }

    dataList = []
    for lat,long in progressbar.progressbar(coords):
        data = request_objects_around_coordinate(lat, long, mapNumber=descr['map_number'])
        v = 0 if data['objectIds'] is None else len(data['objectIds'])
        ret_obj = {'type': descr['cat'], 'lat': lat, 'long': long, 'value': v, 'category': descr['cat']}
        dataList.append(ret_obj)

        #print("Len: ", len(data['objectIds']))
        #pprint(ret_obj)

    fname = "POI_{}_{}.csv".format(descr['cat'], descr['cat'])
    with open(fname, 'w', newline='') as csvfile:
        fieldnames = ['type', 'lat', 'long', 'value', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for o in dataList:
            writer.writerow(o)

        print("Writen: ", fname)

    print("HelloWorld")