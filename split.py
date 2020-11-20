import joblib
import csv
import math
import time
import os
import random
from datetime import datetime
from mapper import mapper
from reducer import reducer


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

# Config
num_para_jobs = 4

# Allow us to start jobs in parallel easily


def parallelize(func, arr):
    return joblib.Parallel(n_jobs=num_para_jobs)(joblib.delayed(func)(tgt) for tgt in arr)


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


if __name__ == '__main__':
    prog_start = time.time()
    with open('../data/Vehicle_GPS_Data__Department_of_Public_Services.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        # Les points sont triés par heure
        points = sorted(reader, key=lambda row: row[4], reverse=True)
        del points[0]
        print(cline)
        print("📄 Treating csv file with" + bcolors.OKGREEN,
              len(points), bcolors.ENDC + "points")
        print(cline)
        print(bcolors.BOLD + "Splitting dataset" + bcolors.ENDC)
        start = time.time()
        trips = []
        # Pour chacuns des points du CSV si leurs trip existe déjà on l'y ajoute sinon on créer un nouveau trip
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
        end = time.time()
        print(cline)
        print(bcolors.BOLD+"Splitting ended in ⏳"+bcolors.OKGREEN, round(end - start, 3),
              bcolors.ENDC + bcolors.BOLD + "seconds !" + bcolors.ENDC)
        print(cline)
        print("🚗 We identified"+bcolors.OKGREEN, len(
            trips), bcolors.ENDC+"differents trips.", )
        # Trips are split to be send to mappers
        batch_size = int(len(trips) / num_para_jobs)
        print("🔀 The trips are going to be processed by" + bcolors.OKBLUE,
              num_para_jobs, bcolors.ENDC + "process, each trating ~"+bcolors.OKGREEN, batch_size, bcolors.ENDC+"trips.")
        print(cline)
        # Jobs are started in parallel

        n = 0
        trips_map = []
        for i in range(0, num_para_jobs):
            first_tip = n
            last_trip = len(trips)-1 if (
                i == num_para_jobs-1) else n + batch_size
            n = last_trip + 1
            trips_map.append(trips[first_tip:last_trip])
        start = time.time()
        results = parallelize(mapper, trips_map)
        end = time.time()

        print(cline)
        print(bcolors.BOLD+"Mapping ended in ⏳"+bcolors.OKGREEN, round(end - start, 3),
              bcolors.ENDC + bcolors.BOLD + "seconds !" + bcolors.ENDC)
        print(cline)
        print(bcolors.BOLD+"Now starting reducers : "+bcolors.ENDC)

        start = time.time()
        results2 = parallelize(reducer, results)
        end = time.time()

        for item in results2:
            if not item:
                results2.remove(item)

        print(cline)
        print(bcolors.BOLD+"Reducing ended in ⏳"+bcolors.OKGREEN, round(end - start, 3),
              bcolors.ENDC + bcolors.BOLD + "seconds !" + bcolors.ENDC)
        print(bcolors.BOLD+"Found"+bcolors.OKGREEN, len(results2),
              bcolors.ENDC + bcolors.BOLD + "candidates :" + bcolors.ENDC)

        for trip in results2:
            print(cline)
            print("🛣️ Trip id" + bcolors.OKGREEN, trip.id,
                  bcolors.ENDC + "with" + bcolors.OKGREEN, len(trip.points), bcolors.ENDC + "points")
            print("📏 Precision" + bcolors.OKBLUE,
                  trip.precision, bcolors.ENDC)
            print("📍 Start point : id " + bcolors.OKGREEN, trip.start_point_id,
                  bcolors.ENDC+"Distance from start :"+bcolors.OKBLUE, trip.start_point_distance, bcolors.ENDC)
            print("📍 End point : id " + bcolors.OKGREEN, trip.end_point_id,
                  bcolors.ENDC+"Distance from end:"+bcolors.OKBLUE, trip.end_point_distance, bcolors.ENDC)
            print("⏳ Time : " + bcolors.OKBLUE,
                  trip.end_timespan, bcolors.ENDC)

        print(cline)
        print(bcolors.BOLD+"Now starting final selection : "+bcolors.ENDC)

        start = time.time()
        overall_best_trip = reducer(results2)
        end = time.time()
        prog_end = time.time()
        print(cline)
        print(bcolors.BOLD+"Final selection ended in ⏳"+bcolors.OKGREEN, round(end - start, 3),
              bcolors.ENDC + bcolors.BOLD + "seconds !" + bcolors.ENDC)
        print(bcolors.BOLD+"Whole program ended in ⏳"+bcolors.OKGREEN, round(prog_end - prog_start, 3),
              bcolors.ENDC + bcolors.BOLD + "seconds !" + bcolors.ENDC)
        print(cline)

        print(bcolors.HEADER+"🏆", "Best trip selected", "🏆"+bcolors.ENDC)
        print("🛣️  Trip id" + bcolors.OKGREEN, overall_best_trip.id,
              bcolors.ENDC + "with" + bcolors.OKGREEN, len(overall_best_trip.points), bcolors.ENDC + "points")
        print("📏 Precision" + bcolors.OKBLUE,
              overall_best_trip.precision, bcolors.ENDC)
        print("📍 Start point : id " + bcolors.OKGREEN, overall_best_trip.start_point_id,
              bcolors.ENDC+"Distance start:"+bcolors.OKBLUE, overall_best_trip.start_point_distance, bcolors.ENDC)
        print("📍 End point : id " + bcolors.OKGREEN, overall_best_trip.end_point_id,
              bcolors.ENDC+"Distance end:"+bcolors.OKBLUE, overall_best_trip.end_point_distance, bcolors.ENDC)
        print("⏳ Time : " + bcolors.OKBLUE,
              overall_best_trip.end_timespan, bcolors.ENDC)
#  🚗
