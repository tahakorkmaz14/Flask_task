from flask import Blueprint, request, abort
from flask import json
from flask.json import jsonify
from flask.wrappers import Response
import requests
import math
from xml.etree import ElementTree
from math import sin, cos, sqrt, atan2, radians
import logging

# approximate radius of earth in km
R = 6373.0


# calculates the distance in kms between the two geolocations


def calculate_distance_in_km(lon1, lon2, lat1, lat2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance - 20


api = Blueprint('api', __name__, url_prefix='/api')

# my api key
api_key = "5c1a9f36-27ef-4048-95c3-2d1d4bfa0154"

# MKAD center location
mkad_long = 55.751771
mkad_lat = 37.619580

# base url
base_url = "https://geocode-maps.yandex.ru/1.x/"

# method for getting the sent location's geolocation


def get_geolocation(address):

    geolocation_api = f"{base_url}?apikey={api_key}&lang=en_US&geocode={address}"

    # sending get request and saving the response as response object
    response = requests.get(url=geolocation_api, stream=True)

    response.raw.decode_content = True

    events = ElementTree.iterparse(response.raw)

    for event, elem in events:
        # do something with `elem`
        if "pos" in elem.tag:
            #print(elem.tag, elem.text)
            return elem.text
    logging.warning("No location has been found")
    return("No location has been found")
    # extracting data in json format

# main handler for requests.
# User need to send the location as a post request to
# http://localhost:5000/api/api/calculate_distance as a json body


@api.route('/api/calculate_distance', methods=['POST'])
def calculate_distance():
    # Error handling here if no address is sent
    if not request.data.decode("utf-8"):
        logging.error("invalid input")
        abort(400, description="invalid input")

    # print(json.loads(request.data.decode("utf-8")))
    address = json.loads(request.data.decode("utf-8"))
    # print(address['address'])

    location = get_geolocation(address["address"])
    lat, long = location.split()
    #print(lat, long)
    lat = float(lat)
    long = float(long)

    # handling invalid address input
    if lat < -180 or lat > 180 or long < -90 or long > 90:
        return(f"<h1>Invalid address!</h1>")

    distance_to_mkad = math.sqrt(
        (lat - mkad_lat) ** 2 + (long - mkad_long) ** 2)

    # radial distance
    min_dist = 0.21940295285900654
    if distance_to_mkad > 0.21940295285900654:
        distance_as_km = "{:.2f}".format(
            calculate_distance_in_km(mkad_long, long, mkad_lat, lat))
        return(f"<h1>The {address['address']} is out of MKAD ring! The distance is {distance_as_km}km</h1>")
    else:
        logging.info(f"The {address['address']} is inside of MKAD ring!")
        return(f"<h1>The {address['address']} is inside of MKAD ring!</h1>")
    # Calculating distance
