## Get list of all available resources/devices for an entity

import requests
import pprint
import json
import pandas as pd
import time
import datetime
from progressbar import ProgressBar


def getListIOTEntities(api_url):
    url = api_url + "/v2/types"
    r = requests.get(url, verify=False)
    j = r.json()
    entity_list = []
    for item in j:
        # print(item['type'])
        entity_list.append(item['type'])
    return (entity_list)


def getResourceList(api_url, entity_name):
    # First let's the ID's from the FiWare
    url = api_url + "/v2/entities?type=" + entity_name
    # print(url)
    r = requests.get(url, verify=False)
    j = r.json()
    # print(j)
    resources_list = []
    for resource in j:
        resources_list.append(resource['id'])
    return (resources_list)


def convertJSONHistoricalToDF(j, entity=None):
    #print(entity)
    if ((entity is None) or (entity is "NoiseLevelObserved") or (entity is "AirQualityObserved")):
        df = pd.DataFrame()
        for i in range(0, len(j['data']['attributes'])):
            df[j['data']['attributes'][i]['attrName']] = j['data']['attributes'][i]['values']
        ## expand location attributes
        # for key in df['location'][0].keys():
        #    df[key] = str(df['location'][0][key])
        df['long'] = df['location'][0]['coordinates'][0]
        df['lat'] = df['location'][0]['coordinates'][1]
        df['device_id'] = j['data']['entityId']
        # print(df)
    elif (entity is "TrafficFlowObserved"):
        df = pd.DataFrame()
        df['intensity'] = [j['intensity']]
        df['dateObserved'] = [j['dateobservedfrom']]
        df['long'] = [j['location']['coordinates'][0]]
        df['lat'] = [j['location']['coordinates'][1]]
    elif (entity is "WeatherObserved"):
        df = pd.DataFrame()
        for i in range(0, len(j['data']['attributes'])):
            df[j['data']['attributes'][i]['attrName']] = j['data']['attributes'][i]['values']
        df['long'] = df['location'][0]['coordinates'][0]
        df['lat'] = df['location'][0]['coordinates'][1]
        df['device_id'] = j['data']['entityId']
    else:
        raise Exception("Wrong json template specified")
    return (df)


def getHistoricalData(api_url, device_id=None, no=20, output="json"):
    if (device_id is not None):
        url = api_url + "/v2/entities/" + device_id + "?limit=" + str(no)
    else:
        raise Exception("device_id is required")

    r = requests.get(url, verify=False)
    j = r.json()

    if "error" not in j:
        if (output is "json"):
            return (j)
        elif (output is "df"):
            return (convertJSONHistoricalToDF(j, entity))
        else:
            raise Exception("invalid output")

def convert_df_to_unix(s):
    time_mask = "%Y-%m-%dT%H:%M:%S.%fZ"
    return (time.mktime(datetime.datetime.strptime(s, time_mask).timetuple()))


## ---------------------------

df = pd.DataFrame()
file_path = "output/ettrafficflowobserved_0_.json"

with open(file_path) as f:
    i =1
    for line in f:
        j = json.loads(line)
        entity = "TrafficFlowObserved"
        df1 = convertJSONHistoricalToDF(j, entity)
        #print(df1)
        if df1 is not None:
            if df.empty:
                df = df1.copy()
            else:
                df = pd.concat([df,df1], sort=False)
        i = 1 + i
        print(i)

## Convert timestamp to unixtime
df['time'] = list(map(convert_df_to_unix, df['dateObserved']))

## Save columns to csv in a custom order
mandatory_column_list = ["time", "lat", "long"]

if (entity is "AirQualityObserved"):
    data_column_list = ["CO", "NO2", "O3", "Ox", "PM1", "PM10", "PM25"]
    for data_column in data_column_list:
        filepath = "./output/" + "IOT_" + "AirQuality_" + data_column + ".csv"
        print(filepath)
        df.to_csv(filepath, columns=mandatory_column_list + [data_column],
                  index=False, na_rep="", header=True)

elif (entity is "NoiseLevelObserved"):
    data_column_list = ["LAeq"]

    for data_column in data_column_list:
        filepath = "./output/" + "IOT_" + "NoiseLevelObserved_" + data_column + ".csv"
        print(filepath)
        df.to_csv(filepath, columns=mandatory_column_list + [data_column],
                  index=False, na_rep="", header=True)
elif (entity is "TrafficFlowObserved"):
    data_column_list = ["intensity"]

    for data_column in data_column_list:
        filepath = "./output/" + "IOT_" + "TrafficFlowObserved_" + data_column + ".csv"
        #print(filepath)
        df.to_csv(filepath, columns=mandatory_column_list + [data_column],
                  index=False, na_rep="", header=True)
elif (entity is "WeatherObserved"):
    data_column_list = ['barometricPressure', 'precipitation', 'relativeHumidity',
                        'solarRadiation', 'temperature', 'windDirection', 'windSpeed']

    for data_column in data_column_list:
        filepath = "./output/" + "IOT_" + "WeatherObserved_" + data_column + ".csv"
        print(filepath)
        df.to_csv(filepath, columns=mandatory_column_list + [data_column],
                  index=False, na_rep="", header=True)