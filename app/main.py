from gpsMapReduce import gpsMapReduce
from classes.Ride import Ride
from classes.Trip import Trip
import classes.Utils as utils
import sys
import time
import configparser
from flask import Flask, jsonify, abort, request
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
csvFile = config['CONFIG']['CsvFile']


@app.route('/trip', methods=['POST'])
def getTrip():
    if not request.json:
        abort(400)
    start_lat = request.json['start_lat']
    start_lon = request.json['start_lon']
    end_lat = request.json['end_lat']
    end_lon = request.json['end_lon']
    if 'min_precision' in request.json:
        min_precision = request.json['min_precision']
    else:
        min_precision = float(config['DEFAULT']['MinPrecision'])
    if 'nbProcess' in request.json:
        nbProcess = request.json['nbProcess']
    else:
        nbProcess = int(config['DEFAULT']['NbProcess'])
    start = time.time()
    trip: Trip = gpsMapReduce(start_lat, start_lon, end_lat,
                              end_lon, min_precision, nbProcess)
    end = time.time()
    print(utils.cline)
    print(utils.BOLD+"WHole process ended in ⏳"+utils.OKGREEN, round(end - start, 3),
          utils.ENDC + utils.BOLD + "seconds !" + utils.ENDC)
    return jsonify(trip), 200


if __name__ == '__main__':
    app.run(debug=True)
