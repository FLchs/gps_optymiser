import os
import configparser
from classes.Trip import Trip
from classes.Point import Point
import classes.Utils as utils

config = configparser.ConfigParser()
config.read('config.ini')
nbProcess = int(config['CONFIG']['NbProcess'])


def parser(points):
    print("⚙️  Parsing process"+utils.OKGREEN,
          os.getpid(), utils.ENDC + "started")
    trips = []

    # Add the point to an existing trip or creating a new one if it doesn't exist
    for point in points:
        new_point = Point(point[0], point[2], point[3], point[4])
        exists = False
        for trip in trips:
            if (trip.id == point[1]):
                trip.points.append(new_point)
                exists = True
        if (exists == False):
            new_trip = Trip(point[1], [new_point])
            trips.append(new_trip)
    return trips
