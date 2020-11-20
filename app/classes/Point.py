from datetime import datetime


class Point:
    def __init__(self, id, lat, lon, dtime):
        self.id = id
        self.lat = float(lat)
        self.lon = float(lon)
        self.dtime = datetime.strptime(dtime, '%m/%d/%Y %H:%M:%S %p')
