from datetime import datetime
import os
import sys
import configparser
import classes.Utils as utils
from classes.Trip import Trip
from classes.Point import Point


def reducer(trips, min_precision):
    print("⚙️  Reducer process"+utils.OKGREEN,
          os.getpid(), utils.ENDC + "started")
    best_trip_time = sys.maxsize
    best_precision = float(sys.maxsize)
    for trip in trips:
        if ((trip.end_timespan < best_trip_time) and (trip.precision < best_precision) and (trip.precision < min_precision)):
            best_precision = trip.precision
            best_trip = trip
            best_trip_time = trip.end_timespan

    err = False
    try:
        if not hasattr(best_trip, 'id'):
            err = True
    except:
        err = True
    if not err:
        return best_trip
