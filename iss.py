#!/usr/bin/env python

__author__ = 'katran009 and google'

import json
import urllib.request
import turtle
import time

# API addresses
ASTRONAUTS_URL = 'http://api.open-notify.org/astros.json'
LOCATION_URL = 'http://api.open-notify.org/iss-now.json'

# Image paths
BACKGROUND_PATH = 'images/map.gif'
ISS_PATH = 'images/iss.gif'


ISS = turtle.Turtle()
WORLD = turtle.Screen()


def api_data(url):
    """
    Get the JSON data from the specified NASA API.
    """
    url = url
    response = urllib.request.urlopen(url)
    # data came as bytes so convert into string to be parsed
    string_response = response.read().decode("utf-8")
    result = json.loads(string_response)

    if result['message']:
        return result
    else:
        return "Something went wrong."


def display_craft_passengers():
    """
    Show number of astronauts and name of astronauts.
    """
    astros_data = api_data(ASTRONAUTS_URL)
    number_astronauts = astros_data['number']
    message = "There are " + str(number_astronauts) + \
        " astronauts in space: \n"
    # Save all astronauts plus a new line in a list
    iss_passengers = [astronaut['name'] +
                      "\n" for astronaut in astros_data['people']]

    for person in iss_passengers:
        message += person

    return(message)


def craft_location():
    """
    Pull craft location sats from NASA API. Return latitude and longitude.
    """
    craft_data = api_data(LOCATION_URL)
    location = craft_data['iss_position']
    lat = location['latitude']
    lon = location['longitude']

    return float(lon), float(lat)


def move_iss():
    """Update iss location on map."""
    ISS.penup()
    lon, lat = craft_location()
    ISS.goto(lon, lat)
    print(lon, lat)


def draw_iss():
    """
    Draw iss thumbnail to the given screen.
    """
    WORLD.register_shape(ISS_PATH)
    ISS.shape(ISS_PATH)
    ISS.setheading(90)

    move_iss()


def draw_map(background):
    """
    Draw map gif in new window.
    """
    WORLD.setup(720, 360)
    WORLD.setworldcoordinates(-180, -90, 180, 90)
    WORLD.bgpic(background)

    draw_iss()


if __name__ == "__main__":
    draw_map(BACKGROUND_PATH)
    turtle.done()
