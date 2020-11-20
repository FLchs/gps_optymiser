from datetime import datetime
import os


class Trip:
    def __init__(self, id, points=[]):
        self.id = id
        self.points = points
        self.start_point_id = int
        self.start_point_distance = 0.0
        self.end_point_id = int
        self.end_point_distance = 0.0
        self.end_timespan = int
        self.precision = 0.0


class Point:
    def __init__(self, id, lat, lon, dtime):
        self.id = id
        self.lat = float(lat)
        self.lon = float(lon)
        self.dtime = datetime.strptime(dtime, '%m/%d/%Y %H:%M:%S %p')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


cline = "--------------------------------------------------------------------------------"

min_precision = 0.005


def reducer(trips):
    print("⚙️  Reducer process"+bcolors.OKGREEN,
          os.getpid(), bcolors.ENDC + "started")
    best_trip_time = 99999
    best_precision = 99999.0
    for trip in trips:
        # if ((trip.end_timespan.seconds < best_trip_time) and (trip.end_timespan.seconds > 0)):
        if ((trip.end_timespan.seconds < best_trip_time) and (trip.precision < best_precision) and (trip.precision < min_precision)):
            best_precision = trip.precision
            best_trip = trip
            best_trip_time = trip.end_timespan.seconds

    err = False
    try:
        if not hasattr(best_trip, 'id'):
            err = True
    except:
        err = True
    if not err:
        return best_trip
