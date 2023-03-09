class Room(object):
    """Defines a room with given inputs"""
    def __init__(self, name, wall, floor, shape):
        self.name = name
        self.wall = wall
        self.floor = floor
        self.shape = shape
        self.features = []

    def add_feature(self, feature):
        """Adds a feature object to a room."""
        self.features.append(feature)