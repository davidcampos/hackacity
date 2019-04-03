from elasticsearch import Elasticsearch

from Impact import Impact


# Category Weather, Temperature
def impact_weather_temperature(value):
    if value >= 0 and value <= 30:
        return Impact.POSITIVE.value
    else:
        return Impact.NEGATIVE.value


def impact_weather_humidity(value):
    if value >= 40 and value <= 69:
        return Impact.POSITIVE.value
    elif value >= 70 and value <= 99 or value >= 0 and value <= 39:
        return Impact.NEGATIVE.value


def impact_weather_pressure(value):
    return Impact.POSITIVE.value


def impact_weather_wind(value):
    return Impact.POSITIVE.value


# Category Traffic
def impact_traffic(value):
    if value >= 0 and value <= 9:
        return Impact.PERFECT.value
    elif value >= 10 and value <= 19:
        return Impact.POSITIVE.value
    elif value >= 20 and value <= 29:
        return Impact.NEUTRAL.value
    elif value >= 30 and value <= 39:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category Noise
def impact_noise(value):
    if value >= 0 and value <= 33:
        return Impact.PERFECT.value
    elif value >= 34 and value <= 42:
        return Impact.POSITIVE.value
    elif value >= 43 and value <= 51:
        return Impact.NEUTRAL.value
    elif value >= 52 and value <= 60:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category AIR, Measure PM2.5
def impact_air_pm25(value):
    if value >= 0 and value <= 15.4:
        return Impact.PERFECT.value
    elif value >= 15.5 and value <= 40.4:
        return Impact.POSITIVE.value
    elif value >= 40.5 and value <= 65.4:
        return Impact.NEUTRAL.value
    elif value >= 65.5 and value <= 150.4:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category AIR, Measure PM10
def impact_air_pm10(value):
    if value >= 0 and value <= 54:
        return Impact.PERFECT.value
    elif value >= 55 and value <= 154:
        return Impact.POSITIVE.value
    elif value >= 155 and value <= 254:
        return Impact.NEUTRAL.value
    elif value >= 255 and value <= 354:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category AIR, Measure CO2
def impact_air_co2(value):
    if value >= 0 and value <= 350:
        return Impact.PERFECT.value
    elif value >= 351 and value <= 599:
        return Impact.POSITIVE.value
    elif value >= 600 and value <= 999:
        return Impact.NEUTRAL.value
    elif value >= 1000 and value <= 1199:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category AIR, Measure O3
def impact_air_o3(value):
    if value >= 0 and value <= 50:
        return Impact.PERFECT.value
    elif value >= 51 and value <= 98:
        return Impact.POSITIVE.value
    elif value >= 99 and value <= 118:
        return Impact.NEUTRAL.value
    elif value >= 119 and value <= 392:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


# Category AIR, Measure NO2
def impact_air_no2(value):
    if value >= 0 and value <= 42:
        return Impact.PERFECT.value
    elif value >= 43 and value <= 94:
        return Impact.POSITIVE.value
    elif value >= 95 and value <= 295:
        return Impact.NEUTRAL.value
    elif value >= 296 and value <= 667:
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


def get_iot_average(type, lat, long, distance):
    res = es.search(ELASTIC_INDEX_IOT, body={
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "type": type
                        }
                    }
                ],
                "filter": {
                    "geo_distance": {
                        "distance": distance,
                        "location": {
                            "lat": lat,
                            "lon": long
                        }
                    }
                }
            }
        },
        "aggs": {
            "avg_type": {"avg": {"field": "value"}}
        }
    })
    return res['aggregations']['avg_type']['value']


def is_poi_available(type, lat, long, distance):
    res = es.search(ELASTIC_INDEX_POI, body={
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "type": type
                        }
                    }
                ],
                "filter": {
                    "geo_distance": {
                        "distance": distance,
                        "location": {
                            "lat": lat,
                            "lon": long
                        }
                    }
                }
            }
        }
    })

    return len(res['hits']['hits']) > 0


ELASTIC_URI = "http://10.250.0.239:9200"
ELASTIC_INDEX_IOT = "hackacity-iot"
ELASTIC_INDEX_POI = "hackacity-poi"

es = Elasticsearch([ELASTIC_URI])


def main():
    # Distances in KM
    config = {
        'air': {
            'distance': 2,
            'weight': 0.1
        },
        'weather': {
            'distance': 2,
            'weight': 0.1
        },
        'traffic': {
            'distance': 3,
            'weight': 0.1
        },
        'noise': {
            'distance': 2,
            'weight': 0.1
        },
        'transports': {
            'distance': 1,
            'weight': 0.1
        },
        'risks': {
            'distance': 2,
            'weight': 0.1
        },
        'markets': {
            'distance': 1.5,
            'weight': 0.1
        },
        'schools': {
            'distance': 1.5,
            'weight': 0.1
        },
        'health': {
            'distance': 1.5,
            'weight': 0.1
        },
        'greenzones': {
            'distance': 1.5,
            'weight': 0.1
        },
        'bairros': {
            'distance': 2,
            'weight': 0.1
        }
    }

    avg_co = get_iot_average('CO', 41.161386, -8.612680, "0.5km")
    print(avg_co)

    has_greenzone = is_poi_available('GREENZONE', 41.161386, -8.612680, "0.5km")
    print(has_greenzone)

    # for hit in res['hits']['hits']:
    #     type = hit["_source"]['type']
    # value = hit["_source"]['value']
    # lat = hit["_source"]['location']['lat']
    # lon = hit["_source"]['location']['lon']
    #
    # print("%s %s %s %s" % (type, value, lat, lon))

    # pprint(res)

    # print(impact_air_co2(500))
    # print(config['air']['distance'])

    # 200mx200m
    # Left Top: 41.188843, -8.712637
    # Left Bottom: 41.131386, -8.712680
    # Right Top: 41.208026, -8.559292
    # Right Bottom: 41.135018, -8.558663
    # i = 0
    # for lat in numpy.arange(41.131386, 41.208026, 0.0018):
    #     for long in numpy.arange(-8.712680, -8.558663, 0.0025):
    #         i = i + 1
    #         print("%s, %s" % (lat, long))
    #
    # print(i)


main()
