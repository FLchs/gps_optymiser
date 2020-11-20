import os
import configparser
from classes.Trip import Trip
from classes.Point import Point
import classes.Utils as utils

config = configparser.ConfigParser()
config.read('config.ini')
nbProcess = int(config['CONFIG']['NbProcess'])


def splitter(trips):
    print("⚙️  Splitting process"+utils.OKGREEN,
          os.getpid(), utils.ENDC + "started")
    # Split the trips to give the same workload to each process
    n = 0
    batch_size = int(len(trips) / nbProcess)
    trips_map = []
    for i in range(0, nbProcess):
        first_tip = n
        last_trip = len(trips)-1 if (
            i == nbProcess-1) else n + batch_size
        n = last_trip + 1
        trips_map.append(trips[first_tip:last_trip+1])
    return trips_map
