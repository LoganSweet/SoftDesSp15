"""

UNFINISHED: The get j_son and get_lat_long functions are finished and working:
I need to finishe the rest so that a place/ address input will return the 
distnace and name off the closest MBTA stop. 








Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


url = "https://maps.googleapis.com/maps/api/geocode/json?address=Fenway%20Park"

# A little bit of scaffolding if you want to use it

def get_placeurl(place_name):


    return 0


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    pprint(response_data)
    #print response_data["results"][0]["formatted_address"]


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    f = urllib2.urlopen(url)
    #f = urllib2.urlopen(get_placeurl(place_name))
    response_text = f.read()
    data = json.loads(response_text)
    #pprint(response_data)
    latlon = data["results"][0]["geometry"]["location"]
    #print latlon
    #print type(latlon)
    latlontup = (latlon[u'lat'], latlon[u'lng'])
    #print latlontup
    return latlontup



def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    pass


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    pass


get_lat_long(url)


