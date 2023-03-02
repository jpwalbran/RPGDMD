class Floor(object):
    """Defines a dungeon floor."""
    def __init__(self, name, wall, floor):
        self.name = name
        self.wall = wall
        self.floor = floor
        self.rooms = []
    
    def add_room(self, r):
        """Adds a room to a floor"""
        self.rooms.append(r)