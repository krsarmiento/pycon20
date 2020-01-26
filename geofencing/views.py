import os, json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from elasticsearch import Elasticsearch
import requests

ELASTIC_URL = 'localhost'
INDEX_NAME = 'lentti'
ES_HOST = 'es01'
ES_PORT = 9200
ES_URL = 'http://{}:{}/{}'.format(ES_HOST, ES_PORT, INDEX_NAME)


def elastic_setup(request):
    setup_result = {}
    elastic_search = Elasticsearch([ES_HOST], port=ES_PORT)

    mapping_file = open(os.path.dirname(os.path.realpath(__file__)) + '/../mapping.json')
    mapping = json.loads(mapping_file.read())
    mapping_file.close()

    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + '/../polygons.json')
    polygons = json.loads(polygons_file.read())
    polygons_file.close()

    index_creation_result = requests.put(ES_URL, json=mapping, headers={'Content-Type': 'application/json'})
    setup_result['index_creation'] = index_creation_result.json()

    place = {
        "name": None,
        "active": True,
        "location": {
            "type": "polygon",
            "coordinates": []
        }
    }

    polygon_upload_results = []
    for polygon in polygons:
        place["name"] = polygon["name"]
        place["canonical_name"] = polygon["canonical_name"]
        place["schedule"] = polygon["schedule"]
        place["location"]["coordinates"] = polygon["coordinates"]
        res = elastic_search.index(index=INDEX_NAME, body=place)
        polygon_upload_results.append(res)

    setup_result['polygon_upload'] = polygon_upload_results
    return JsonResponse(setup_result)


def search(request):
    elastic_search = Elasticsearch([ES_HOST], port=ES_PORT)

    range_filters = [
        {"range": {"schedule.starts": {"lte": 720}}},
        {"range": {"schedule.ends": {"gte": 720}}},
    ]

    nested_query = {
        "nested": {
            "path": "schedule",
            "query": {"bool": {"filter": range_filters}}
        }
    }

    query = {
        "query": {
            "bool": {"must": nested_query}
        }
    }

    coordinates = request.GET.get("coordinates", None)
    if coordinates and coordinates != "None":
        latitude, longitude = coordinates.split(",")
        query["query"]["bool"]["filter"] = {
            "geo_shape": {
                "location": {
                    "shape": {
                        "type": "point",
                        "coordinates": [longitude, latitude]
                    },
                    "relation": "contains"
                }
            }
        }

    import json
    print(json.dumps(query))

    response = []
    res = elastic_search.search(index=INDEX_NAME, body=query)
    for hit in res['hits']['hits']:
        response.append(hit["_source"])

    return JsonResponse(response, safe=False)


def index(request):
    context = {}
    coordinates = request.GET.get("coordinates", None)
    context["coordinates"] = coordinates
    return render(request, 'geofencing/index.html', context)


def dashboard(request):
    context = {}
    coordinates = request.GET.get("coordinates", None)
    context["coordinates"] = coordinates
    return render(request, 'geofencing/dashboard.html', context)
