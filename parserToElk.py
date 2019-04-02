#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import json
import csv
import elasticsearch
import getopt
import sys

def addToElastic(indexSuffix,payload):
    try:
        logging.debug(payload)
        logging.debug(indexSuffix)
        r = requests.post("http://elasticsearch.tz:9200/hackacity-%s/doc"%(indexSuffix,), json=payload)
        logging.debug(r.text)
    except Exception as e:
        logging.error("Failed to push event to elastic: " + str(e))

def getDocuments(index,query={"query": {"match_all": {}}}):
	rs = es.search(index=index, body=query, scroll='10s', preference='_primary_first', size=10000)
	sid=rs['_scroll_id']
	total = rs['hits']['total']
	results = rs['hits']['hits'] 
	while (len(results) < total):
		rs = es.scroll(scroll_id=sid, scroll='10s')
		results += rs['hits']['hits']
		sid=rs['_scroll_id']

	return results

def parseCsvFile_POI(filename):
    index,category,datatype=filename.split("/")[1].split(".")[0].split("_")
    index = index.lower()
    payload = {}
    payload["category"] = category
    payload["type"] = datatype
    with open(filename, mode='r') as csv_file:
        line_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                headers = row
                line_count = 1
                continue
            try:
                payload["date"] = int(row[0].split(".")[0])*1000
                payload["value"] = float(row[3])
                location = {}
                location["lat"] = row[1]
                location["lon"] = row[2]
                payload["location"] = location
            except ValueError as ve:
                logging.error("Failed to parse entry: %s due to %s "%(str(row),str(ve)) )
            addToElastic(index,payload)

if __name__ == '__main__':

    LOGGING_LEVEL = "DEBUG"
    logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)-4s %(message)s')

    es = elasticsearch.Elasticsearch(['http://elasticsearch.tz:9200'],timeout=30)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:e:")
    except getopt.GetoptError, err:
        logging.error("problem with arguments")
        sys.exit(2)

    for o, a in opts:
        if o == "-f":
            filename = a
        elif o == "-e":
            coiso = int(a)
        else:
            sys.exit(2)


    parseCsvFile_POI("output/IOT_AirQuality_CO.csv")