import requests
import numpy
import csv

import progressbar

import get_areas
import json

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

def request_objects_around_coordinate(lat,long, mapNumber=77):
    req_params = _DEFAULT_PARAMS
    req_params['geometry'] = "{}, {}".format(long, lat)

    url = 'https://servsig.cm-porto.pt/arcgis/rest/services/OpenData_APD/OpenData_APD/MapServer/{}/query'.format(mapNumber)
    r = requests.get(url, params=req_params)

    return r.json()

if __name__ == "__main__":
    myEnvelope = {"xmin" : -8.71268, "ymin" : 41.131386, "xmax" : -8.560180000000031, "ymax" : 41.20698600000012}
    get_areas._DEFAULT_PARAMS['geometry'] = json.dumps(myEnvelope)
    get_areas._DEFAULT_PARAMS['geometryType'] = 'esriGeometryEnvelope'
    get_areas._DEFAULT_PARAMS['returnIdsOnly'] = False

    ## Numbers
    knownMaps = [
        {
            'map_number': 48,
            'type': 'Hospital',
            'cat': 'Health'
        },
        {
            'map_number': 49,
            'type': 'CentroDeSaude',
            'cat': 'Health'
        },
        {
            'map_number': 50,
            'type': 'Farmacia',
            'cat': 'Health'
        },
        {
            'map_number': 63,
            'type': 'PreEscolar',
            'cat': 'School'
        },
        {
            'map_number': 65,
            'type': 'Basico',
            'cat': 'School'
        },
        {
            'map_number': 67,
            'type': 'Secundario',
            'cat': 'School'
        },
        {
            'map_number': 69,
            'type': 'Universitario',
            'cat': 'College'
        },
        {
            'map_number': 26,
            'type': 'SuperMercado',
            'cat': 'Market'
        }
    ]

    for descr  in knownMaps:
        print("HelloWorld")

        data = get_areas.request_objects(json.dumps(myEnvelope), mapNumber=descr['map_number'])

        dataList = []
        for f in data['features']:
            l0 = f['geometry']['y']
            l1 = f['geometry']['x']

            ret_obj = {'type': descr['type'], 'lat': l0, 'long': l1, 'value': 1, 'category': descr['cat']}
            dataList.append(ret_obj)

        print("Writting CSV")
        get_areas.write_csv(descr['cat'], dataList, t=descr['type'])

        print("Found", len(dataList), "POIs")
