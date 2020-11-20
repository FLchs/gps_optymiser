import os
import time
import random
import math
import sys
from datetime import datetime
import classes.Utils as utils
from classes.Trip import Trip
from classes.Point import Point
from classes.Ride import Ride


def mapper(trips, ride):
    end_lat = ride.end_lat
    end_lon = ride.end_lon
    start_lat = ride.start_lat
    start_lon = ride.start_lon
    print("⚙️  Mapping process"+utils.OKGREEN,
          os.getpid(), utils.ENDC + "started")
    for trip in trips:
        #  Variables initialisation
        best_start_point_id = -1
        best_start_point_distance = float(sys.maxsize)
        best_end_point_id = -1
        best_end_point_distance = float(sys.maxsize)
        for point in trip.points:
            distance_from_start = ((((point.lat - start_lat)**2) +
                                    ((point.lon - start_lon) ** 2)) ** 0.5)
            distance_from_end = ((((point.lat - end_lat)**2) +
                                  ((point.lon - end_lon) ** 2)) ** 0.5)
            # Check if we have a starting point candidate
            if (distance_from_start < best_start_point_distance):
                best_start_point_id = trip.points.index(point)
                best_start_point_distance = distance_from_start
            # Check if we have an endpoint candidate
            if (distance_from_end < best_end_point_distance):
                best_end_point_id = trip.points.index(point)
                best_end_point_distance = distance_from_end

        points_temp = trip.points[best_start_point_id:best_end_point_id+1]
        if len(points_temp) == 0:
            points_temp = trip.points[best_end_point_id:best_start_point_id + 1]

        trip.points = points_temp
        trip.start_point_id = best_start_point_id
        trip.start_point_distance = best_start_point_distance
        trip.end_point_id = best_end_point_id
        trip.end_point_distance = best_end_point_distance
        trip.end_timespan = (
            trip.points[0].dtime - trip.points[len(trip.points)-1].dtime).seconds
        trip.precision = (trip.start_point_distance +
                          trip.end_point_distance)/2
    res = []
    for trip in trips:
        # Removing trip if both starting and ending points are the same or if there is only 2 points
        if not ((trip.start_point_id == trip.end_point_id) and (len(trip.points) == 2)):
            res.append(trip)
    return res
