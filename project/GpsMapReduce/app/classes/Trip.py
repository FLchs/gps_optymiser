class Trip:
    def __init__(self, id, points=[]):
        self.id = id
        self.points = points
        self.start_point_id = int()
        self.start_point_distance = 0.0
        self.end_point_id = int()
        self.end_point_distance = 0.0
        self.end_timespan = int()
        self.precision = 0.0
