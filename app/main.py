# from flask import Flask
import csv
import math
# app = Flask(__name__)


class Asset:
    def __init__(self, id, points=[]):
        self.id = id
        self.points = points
        self.distOri = 0
        self.oriId = 0
        self.distDest = 0
        self.destId = 0


class Point:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.distOri = 0
        self.distDest = 0


if __name__ == '__main__':
    origin = Point(0, 39.111, -84.776)
    destination = Point(0, 39.130, -84.544)
    print("## Route ## \nfrom : " + str(origin.lat) + " " + str(origin.lon))
    print("to : " + str(destination.lat) + " " + str(destination.lon))
    with open('./data/Vehicle_GPS_Data__Department_of_Public_Services.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        points = sorted(reader, key=lambda row: row[0], reverse=True)
        del points[0]
        lines = 0
        assetid = 0
        assets = []
        for row in points:
            index = 0
            if row[0] != assetid:
                asset = Asset(row[0], [])
                assetid = row[0]
                assets.append(asset)
                index = assets.index(asset)
                pointid = 0
            if row[0] == assetid:
                point = Point(pointid, row[1], row[2])
                assets[index].points.append(point)
                pointid += 1
            # print(row[0])
            lines += 1
            if lines > 50000:
                break
        for asset in assets:
            print("###   Asset id : " + asset.id + "   ###")
            for point in asset.points:

                # Pour chacun des points on calcule ses distances min et max avec l'origin et la destination
                point.distOri = math.sqrt(math.pow(
                    float(point.lat) - float(origin.lat), 2)) + math.sqrt(math.pow(float(point.lon) - float(origin.lon), 2))
                point.distDest = math.sqrt(math.pow(
                    float(point.lat) - float(destination.lat), 2)) + math.sqrt(math.pow(float(point.lon) - float(destination.lon), 2))

                # print(str(point.id) + " : " +
                #       str(point.lat) + " " + str(point.lon) + "\ndist origine : " + str(point.distOri) + "\ndist destination : " + str(point.distDest))
        for asset in assets:
            # print("###   Asset id : " + asset.id + "   ###")
            bestOri = 0
            for point in asset.points:
                if (bestOri == 0):
                    bestOri = point.id

                # print(str(point.id) + " : " +
                #       str(point.distOri) + " " + str(point.distDest))
            asset.bestOri = bestOri

        for asset in assets:
            print("###   Asset id : " + asset.id + "   ###")
            print("Best origin : " + str(asset.bestOri))
    # app.run()


# http://127.0.0.1:5000/route/39.111,-84.776/39.130,-84.544


# class Point:
#     def __init__(self, id, asset, distlon, distlat):
#         self.id = id
#         self.asset = asset
#         self.distlon = distlon
#         self.distlat = distlat
#         self.distot = math.sqrt(math.pow(distlon + distlat, 2))


# def get_dist(point):
#     return point.distot


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# @app.route("/route/<origin>/<destination>")
# def route(origin=None, destination=None):
#     origin = origin.split(",")
#     destination = destination.split(",")

#     points = []

#     with open('./data/Vehicle_GPS_Data__Department_of_Public_Services.csv', newline='\n') as csvfile:
#         reader = csv.reader(csvfile)
#         retour = ""
#         lines = 0

#         print("origin : " + origin[0] + " destination : " + destination[0])
#         for row in reader:
#             if lines == 0:
#                 lines += 1
#                 continue
#             point = Point(lines, int(row[0]), float(
#                 row[1]) - float(origin[0]), float(row[2]) - float(origin[1]))
#             points.append(point)
#             lines += 1
#         points.sort(key=get_dist)
#         retour = "Best start point : " + \
#             str(points[0].id) + "<br>" + "asset :" + \
#             str(points[0].asset) + "<br><br>"
#         asset = points[0].asset
#         for point in points:
#             if (point.asset == asset):
#                 retour += "point : " + str(point.id) + " distance lon : " + \
#                     str(point.distlon) + " distance lat : " + \
#                     str(point.distlat) + " distance totale : " + \
#                     str(point.distot) + "<br>"

#     return retour


# @app.route('/csv')
# def raw_csv():
#     with open('./data/Vehicle_GPS_Data__Department_of_Public_Services.csv', newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         retour = ""
#         lines = 0
#         for row in spamreader:
#             retour += ', '.join(row)
#             lines += 1
#         print(lines)
#         return retour
