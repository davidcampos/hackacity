import multiprocessing as mp

import numpy
from elasticsearch import Elasticsearch

from Impact import Impact


# Category Weather, Temperature
def impact_weather_temperature(value):
    if value == None:
        return Impact.NONE.value

    if value >= 0 and value <= 30:
        return Impact.POSITIVE.value
    else:
        return Impact.NEGATIVE.value


def impact_weather_humidity(value):
    if value == None:
        return Impact.NONE.value

    if value >= 40 and value <= 69:
        return Impact.POSITIVE.value
    elif value >= 70 and value <= 99 or value >= 0 and value <= 39:
        return Impact.NEGATIVE.value


def impact_weather_pressure(value):
    if value == None:
        return Impact.NONE.value

    return Impact.POSITIVE.value


def impact_weather_wind(value):
    if value == None:
        return Impact.NONE.value

    return Impact.POSITIVE.value


# Category Traffic
def impact_traffic(value):
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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
    if value == None:
        return Impact.NONE.value

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


def impact_poi_positive(poi, lat, lon, distance):
    if is_poi_available(poi, lat, lon, str(distance) + "km"):
        return Impact.PERFECT.value
    elif is_poi_available(poi, lat, lon, str(2 * distance) + "km"):
        return Impact.POSITIVE.value
    elif is_poi_available(poi, lat, lon, str(3 * distance) + "km"):
        return Impact.NEUTRAL.value
    elif is_poi_available(poi, lat, lon, str(4 * distance) + "km"):
        return Impact.NEGATIVE.value
    else:
        return Impact.BLOCKER.value


def impact_poi_negative(poi, lat, lon, distance):
    if is_poi_available(poi, lat, lon, str(distance) + "km"):
        return Impact.BLOCKER.value
    elif is_poi_available(poi, lat, lon, str(2 * distance) + "km"):
        return Impact.NEGATIVE.value
    elif is_poi_available(poi, lat, lon, str(3 * distance) + "km"):
        return Impact.NEUTRAL.value
    elif is_poi_available(poi, lat, lon, str(4 * distance) + "km"):
        return Impact.POSITIVE.value
    else:
        return Impact.PERFECT.value


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


def calculate_life_quality(lat, lon):
    # GreenZone
    greenzone = impact_poi_positive('GreenZone', lat, lon, config['GreenZone']['distance'])
    # print("GreenZone: ", Impact(greenzone))

    # School
    school = impact_poi_positive('School', lat, lon, config['School']['distance'])
    # print("School: ", Impact(school))

    # Market
    market = impact_poi_positive('Market', lat, lon, config['Market']['distance'])
    # print("Market: ", Impact(market))

    # Market
    health = impact_poi_positive('Health', lat, lon, config['Health']['distance'])
    # print("Health: ", Impact(health))

    # Bairros
    bairros = impact_poi_negative('Bairros', lat, lon, config['Bairros']['distance'])
    # print("Bairros: ", Impact(bairros))

    # Air
    avg_co = get_iot_average('CO', lat, lon, config['air']['distance'])
    co = impact_air_co2(avg_co)
    # print('CO2: %s' % Impact(impact_air_co2(avg_co)))

    avg_o3 = get_iot_average('O3', lat, lon, config['air']['distance'])
    o3 = impact_air_o3(avg_o3)
    # print('O3: %s' % Impact(impact_air_o3(avg_o3)))

    avg_pm25 = get_iot_average('PM25', lat, lon, config['air']['distance'])
    pm25 = impact_air_pm25(avg_pm25)
    # print('PM25: %s' % Impact(impact_air_pm25(avg_pm25)))

    avg_pm10 = get_iot_average('PM10', lat, lon, config['air']['distance'])
    pm10 = impact_air_pm10(avg_pm10)
    # print('PM10: %s' % Impact(impact_air_pm10(avg_pm10)))

    avg_no2 = get_iot_average('NO2', lat, lon, config['air']['distance'])
    no2 = impact_air_no2(avg_no2)
    # print('NO2: %s' % Impact(impact_air_no2(avg_no2)))

    # air_quality = 5 - numpy.sqrt(
    #     ((5 - co) ^ 2 + (5 - o3) ^ 2 + (5 - pm25) ^ 2 + (5 - pm10) ^ 2 + (5 - no2) ^ 2) / 5)
    air_quality = (co + o3 + pm25 + pm10 + no2) / 5
    # print('AIR QUALITY: %s' % air_quality)

    # Noise
    avg_noise = get_iot_average('LAeq', lat, lon, config['noise']['distance'])
    noise = impact_noise(avg_noise)

    # print('NOISE: %s' % Impact(noise))

    life_quality = \
        config['GreenZone']['weight'] * greenzone + \
        config['School']['weight'] * school + \
        config['Market']['weight'] * market + \
        config['Health']['weight'] * health + \
        config['Bairros']['weight'] * bairros + \
        config['air']['weight'] * air_quality + \
        config['noise']['weight'] * noise

    # print("LIFE QUALITY: ", life_quality)

    doc = {
        "location": {
            "lat": lat,
            "lon": lon
        },
        "value": life_quality,
        "GreenZone": greenzone,
        "School": school,
        "Market": market,
        "Health": health,
        "Bairros": bairros,
        "AirQuality": air_quality,
        "NoiseLevelObserved": noise
    }

    res = es.index(index=ELASTIC_INDEX_RESULT, doc_type='doc', body=doc)
    print(res['result'])
    return True


ELASTIC_URI = "http://10.250.0.239:9200"
ELASTIC_INDEX_IOT = "hackacity-iot"
ELASTIC_INDEX_POI = "hackacity-poi"
ELASTIC_INDEX_RESULT = "hackacity-result"

es = Elasticsearch([ELASTIC_URI])

# Distances in KM
config = {
    'air': {
        'distance': '4km',
        'weight': 0.15
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
        'distance': '1km',
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
    'Market': {
        'distance': 0.5,
        'weight': 0.1
    },
    'School': {
        'distance': 0.5,
        'weight': 0.15
    },
    'Health': {
        'distance': 1,
        'weight': 0.15
    },
    'GreenZone': {
        'distance': 0.25,
        'weight': 0.1
    },
    'Bairros': {
        'distance': 0.1,
        'weight': 0.25
    }
}


def main():
    # GreenZone

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
    coords = []

    # NOT SO BAD
    # for lat in numpy.arange(41.131386, 41.208026, 0.0018):
    #     for lon in numpy.arange(-8.712680, -8.558663, 0.0025):

    for lat in numpy.arange(41.131386, 41.208026, 0.0015):
        for lon in numpy.arange(-8.712680, -8.558663, 0.0015):
            coords.append((lat, lon))

    print("TOTAL: ", len(coords))

    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(32)
    results = [pool.apply_async(calculate_life_quality, args=(lat, lon)) for (lat, lon) in coords]
    pool.close()
    pool.join()


# parallel(n_jobs=8)(delayed(calculate_life_quality)(lat, lon) for lat, lon in coords)

# Parallel(n_jobs=8)(delayed(calculate_life_quality)(lat, lon) for (lat, lon) in coords)


# print(res['result'])

# print()


main()
