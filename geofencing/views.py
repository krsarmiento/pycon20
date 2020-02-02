import os
import json
from datetime import datetime
import requests
import pytz
from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from .schedule import Schedule


ELASTIC_URL = "localhost"
INDEX_NAME = "lentti"
ES_HOST = "es01"
ES_PORT = 9200
ES_URL = "http://{}:{}/{}".format(ES_HOST, ES_PORT, INDEX_NAME)
TIMEZONE = "America/Bogota"


def elastic_setup(request):
    setup_result = {}
    elastic_search = Elasticsearch([ES_HOST], port=ES_PORT)

    mapping_file = open(os.path.dirname(os.path.realpath(__file__)) + "/../mapping.json")
    mapping = json.loads(mapping_file.read())
    mapping_file.close()

    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + "/../polygons.json")
    polygons = json.loads(polygons_file.read())
    polygons_file.close()

    index_creation_result = requests.put(ES_URL, json=mapping, headers={"Content-Type": "application/json"})
    setup_result["index_creation"] = index_creation_result.json()

    polygon_upload_results = []
    for polygon in polygons:
        res = elastic_search.index(index=INDEX_NAME, body=polygon)
        polygon_upload_results.append(res)

    setup_result["polygon_upload"] = polygon_upload_results
    return JsonResponse(setup_result)


def search(request):
    elastic_search = Elasticsearch([ES_HOST], port=ES_PORT)

    match_all = request.GET.get("match_all", None)
    coordinates = request.GET.get("coordinates", None)

    current_datetime = datetime.now(pytz.timezone(TIMEZONE))

    # You might uncomment the following line to specify a datetime (for debugging)
    # current_datetime = datetime.strptime("2020-01-12T20:17:00-05:00", "%Y-%m-%dT%H:%M:%S%z")

    schedule = Schedule(current_datetime)
    numeric_time = schedule.get_numeric_representation()

    schedule_query = {"must": {"match_all": {}}}
    geo_query = {}

    if not match_all:
        range_filters = [
            {"range": {"schedule.starts": {"lte": numeric_time}}},
            {"range": {"schedule.ends": {"gte": numeric_time}}},
        ]

        nested_query = {
            "nested": {
                "path": "schedule",
                "query": {"bool": {"filter": range_filters}}
            }
        }

        schedule_query = {"must": nested_query}

    if coordinates and coordinates != "":
        latitude, longitude = tuple(map(float, coordinates.split(",")))
        geo_query = {
            "filter": {
                "geo_shape": {
                    "location": {
                        "shape": {
                            "type": "point",
                            "coordinates": [longitude, latitude]
                        },
                        "relation": "intersects"
                    }
                }
            }
        }

    search_query = {
        "query": {
            "bool": {
                **schedule_query,
                **geo_query,
            }
        }
    }

    results = []
    res = elastic_search.search(index=INDEX_NAME, body=search_query)
    for hit in res["hits"]["hits"]:
        results.append(hit["_source"])

    response = {
        "results": results,
        "current_datetime": current_datetime.strftime("%A, %b %d @ %H:%M"),
        "numeric_time": numeric_time,
    }

    return JsonResponse(response)


def dashboard(request):
    context = {"querystring": urlencode(request.GET, safe=","), "coordinates": request.GET.get("coordinates", None)}
    return render(request, "geofencing/dashboard.html", context)
