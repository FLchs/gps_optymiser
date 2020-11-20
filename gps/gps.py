
import csv
import math
from datetime import datetime

end_lat = 39.166236
end_lon = -84.514016
start_lat = 39.142305
start_lon = -84.534169


class Trajet:
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
    trajets = []
    # with open('../data/small.csv', newline='\n') as csvfile:
    with open('../data/Vehicle_GPS_Data__Department_of_Public_Services.csv', newline='\n') as csvfile:

        reader = csv.reader(csvfile)
        # Les points sont triés par heure
        points = sorted(reader, key=lambda row: row[4], reverse=True)
        del points[0]
        # Pour chacuns des points du CSV si leurs trajet existe déjà on l'y ajoute sinon on créer un nouveau trajet
        for point in points:
            new_point = Point(point[0], point[2], point[3], point[4])
            exists = False
            for trajet in trajets:
                if (trajet.id == point[1]):
                    trajet.points.append(new_point)
                    exists = True
            if (exists == False):
                new_trajet = Trajet(point[1], [new_point])
                trajets.append(new_trajet)

        # Trouver le meilleur point de départ
        for trajet in trajets:
            best_point_id = ""
            best_point_dist = 9999999999
            for point in trajet.points:
                distance = ((((point.lat - start_lat)**2) +
                             ((point.lon - start_lon) ** 2)) ** 0.5)
                # print("best distance : " + str(best_point_dist) +
                #       " distance actuelle : " + str(distance))
                if (distance < best_point_dist):
                    # print("Point validé car " + str(distance) +
                    #       "<" + str(best_point_dist))
                    best_point_id = trajet.points.index(point)
                    best_point_dist = distance
            trajet.start_point_id = best_point_id
            trajet.start_point_distance = best_point_dist

        #  Trouvé le meilleur point d'arrivé
        for trajet in trajets:
            best_point_id = ""
            best_point_dist = 9999999999
            for point in trajet.points:
                distance = ((((point.lat - end_lat)**2) +
                             ((point.lon - end_lon) ** 2)) ** 0.5)
                # print("best distance : " + str(best_point_dist) +
                #       " distance actuelle : " + str(distance))
                if (distance < best_point_dist):
                    # print("Point validé car " + str(distance) +
                    #       "<" + str(best_point_dist))
                    best_point_id = trajet.points.index(point)
                    best_point_dist = distance
            trajet.end_point_id = best_point_id
            trajet.end_point_distance = best_point_dist
            trajet.end_timespan = (abs(
                trajet.points[trajet.end_point_id].dtime - trajet.points[trajet.start_point_id].dtime))
            trajet.precision = (trajet.start_point_distance +
                                trajet.end_point_distance)/2

        #  Calcul des durées
        # for trajet in trajets:

        # for trajet in trajets:
        #     print(trajet.id)
        #     print("Depart : id ", trajet.start_point_id,
        #           "Distance :", trajet.start_point_distance)
        #     print("Arrivée : id ", trajet.end_point_id,
        #           "Distance :", trajet.end_point_distance)
        #     print("Durée du trajet : ", trajet.end_timespan)
        #     for point in trajet.points:
        #         print(" -- ", point.id)

        best_trajet = Trajet
        best_trajet_time = 99999
        best_precision = 99999.0
        min_precision = 0.002
        for trajet in trajets:
            # if ((trajet.end_timespan.seconds < best_trajet_time) and (trajet.end_timespan.seconds > 0)):
            if ((trajet.end_timespan.seconds < best_trajet_time) and (trajet.precision < best_precision) and (trajet.precision < min_precision)):
                best_precision = trajet.precision
                best_trajet = trajet
                best_trajet_time = trajet.end_timespan.seconds

        print("#######BEST TRAJET#######")
        print(best_trajet.id)
        print("Precision", best_trajet.precision)
        print("Depart : id ", best_trajet.start_point_id,
              "Distance :", best_trajet.start_point_distance)
        print("Arrivée : id ", best_trajet.end_point_id,
              "Distance :", best_trajet.end_point_distance)
        print("Durée du trajet : ", best_trajet.end_timespan)
        for point in best_trajet.points:
            if ((int(best_trajet.points.index(point)) >= int(best_trajet.start_point_id)) and (int(best_trajet.points.index(point)) <= int(best_trajet.end_point_id))
                    or
                    (int(best_trajet.points.index(point)) <= int(best_trajet.start_point_id)) and (
                    int(best_trajet.points.index(point)) >= int(best_trajet.end_point_id))
                ):
                print(" -- ", point.id)
