import configparser
import classes.Utils as utils
import csv
import time
import sys
import parallelize
from MapReduce.splitter import splitter
from MapReduce.parser import parser
from MapReduce.mapper import mapper
from MapReduce.reducer import reducer
from classes.Ride import Ride
from flask import jsonify


config = configparser.ConfigParser()
config.read('config.ini')
csvFile = config['CONFIG']['CsvFile']
nbProcess = int(config['DEFAULT']['NbProcess'])
min_precision = float(config['DEFAULT']['MinPrecision'])


def gpsMapReduce(start_lat, start_lon, end_lat, end_lon, min_precision=min_precision, nbProcess=nbProcess):
    # ride = Ride(39.142305, -84.534169, 39.166236, -84.514016)
    ride = Ride(start_lat, start_lon, end_lat, end_lon)

    if len(sys.argv) >= 5:
        print(sys.argv[1])
    if len(sys.argv) > 1 and len(sys.argv) < 5:
        print(utils.FAIL+"Wrong number of args", utils.ENDC)
        print(utils.BOLD+"Usage : main start_lat, start_lon, end_lat, end_lon, precision", utils.ENDC)
        exit(1)

    with open(csvFile, newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        # Sorting points by time, may be unecessary ?
        points = sorted(reader, key=lambda row: row[4], reverse=True)
        # Removing header
        del points[0]

        print(utils.cline)
        print("📄 Treating csv file with" + utils.OKGREEN,
              len(points), utils.ENDC + "points")
        print(utils.cline)
        print(utils.BOLD + "Parsing dataset" + utils.ENDC)

        ############ Parsing ############
        # Can only be treated by one process as we could split trips paths
        start = time.time()
        # Even though it will be run on only one process, parallelize returns an array so we take the first element
        trips = parallelize.run(1, parser, [points])[0]
        end = time.time()

        print(utils.cline)
        print(utils.BOLD+"Parsing ended in ⏳"+utils.OKGREEN, round(end - start, 3),
              utils.ENDC + utils.BOLD + "seconds !" + utils.ENDC)
        print(utils.cline)
        print("🚗 We identified"+utils.OKGREEN, len(
            trips), utils.ENDC + "differents trips.",)
        print(utils.cline)

        ############ Splitting ############
        print(utils.BOLD + "Spliting dataset :" + utils.ENDC)
        start = time.time()
        # Each batch will be composed of an ~ number of trips
        batch_size = int(len(trips) / nbProcess)
        # Can only be treated by one process as we could split trips paths
        orig_trips_size = len(trips)
        # Even though it will be run on only one process, parallelize returns an array so we take the first element
        trips = parallelize.run(1, splitter, [trips])[0]
        end = time.time()

        print(utils.cline)
        print(utils.BOLD+"Splitting ended in ⏳"+utils.OKGREEN, round(end - start, 3),
              utils.ENDC + utils.BOLD + "seconds !" + utils.ENDC)
        print(utils.cline)

        # Trips are split to be send to mappers
        print("🔀 The trips are going to be processed by" + utils.OKBLUE,
              nbProcess, utils.ENDC + "process, each trating ~"+utils.OKGREEN, batch_size, utils.ENDC+"trips.")
        print(utils.cline)

        ############ Mapping ############
        print(utils.BOLD + "Mapping dataset :" + utils.ENDC)
        start = time.time()
        # Start "nbProcess" mappers, each on it own process, could be sent to differents machines
        trips = parallelize.run_with_args(nbProcess, mapper, ride, trips)
        trips_size = 0
        for trip in trips:
            trips_size = trips_size + len(trip)
        end = time.time()

        print(utils.cline)
        print(utils.BOLD+"Mapping ended in ⏳"+utils.OKGREEN, round(end - start, 3),
              utils.ENDC + utils.BOLD + "seconds !" + utils.ENDC)
        print(utils.cline)
        print("🛣️  The mappers have computed best points for" +
              utils.OKGREEN, trips_size, utils.ENDC+"trips")
        print("🗑️ "+utils.OKCYAN, orig_trips_size-trips_size,
              utils.ENDC+"trips have been filtered")
        print(utils.cline)

        ############ Reducing ############
        # If nothing is found with min precision, lower precision...
        while (True):
            print(utils.BOLD + "Reducing dataset : " + utils.ENDC)
            start = time.time()
            # Start "nbProcess" mappers, each on it own process, could be sent to differents machines
            trips_temp = list(filter(None.__ne__, parallelize.run_with_args(
                nbProcess, reducer, min_precision, trips)))
            if len(trips_temp) < 4:
                if len(trips_temp) == 0:
                    print(utils.WARNING,
                          "No trips found with precision of", min_precision)
                else:
                    print(utils.WARNING, "Onlye", len(trips_temp),
                          "trips found with precision of", min_precision)
                min_precision = min_precision + 0.005
                print(utils.OKCYAN, "Trying with", min_precision)
            else:
                trips = trips_temp
                break

        end = time.time()
        print(utils.cline)
        print(utils.BOLD+"Reducing ended in ⏳"+utils.OKGREEN, round(end - start, 3),
              utils.ENDC + utils.BOLD + "seconds !" + utils.ENDC)
        print(utils.cline)
        print("🏆  The reducers have found a total of" + utils.OKGREEN, len(trips),
              utils.ENDC + "candidates !", utils.ENDC)
        print(utils.OKCYAN, "Precision : ", min_precision, utils.ENDC)
        print(utils.cline)

        ############ Selecting final result ############
        print(utils.BOLD+"Now starting final selection : "+utils.ENDC)
        start = time.time()

        # Start 1 reducer to select the best trip amongs the candidates
        trip = parallelize.run_with_args(1, reducer, min_precision, [trips])[0]

        print(utils.cline)
        print(utils.HEADER+"🥇", "Best trip selected", "🥇"+utils.ENDC)
        print("🛣️  Trip id" + utils.OKGREEN, trip.id,
              utils.ENDC + "with" + utils.OKGREEN, len(trip.points), utils.ENDC + "points")
        print("📏 Precision" + utils.OKBLUE,
              trip.precision, utils.ENDC)
        print("📍 Start point : id " + utils.OKGREEN, trip.start_point_id,
              utils.ENDC+" - Distance from origin :"+utils.OKBLUE, trip.start_point_distance, utils.ENDC)
        print("📍 End point : id " + utils.OKGREEN, trip.end_point_id,
              utils.ENDC+" - Distance from objective :"+utils.OKBLUE, trip.end_point_distance, utils.ENDC)
        print("⏳ Time : " + utils.OKBLUE,
              trip.end_timespan, utils.ENDC, "seconds")

        jpoints = []
        for point in trip.points:
            jpoints.append(
                {"id": point.id, "lat": point.lat, "lon": point.lon})

        result = {
            "id": trip.id,
            "time": str(trip.end_timespan),
            "points": jpoints
        }
        return result
