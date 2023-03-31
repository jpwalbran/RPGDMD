class Floor(object):
    def __init__(self, name, shape, mats, interior):
        self.name = name
        self.shape = shape
        self.mats = mats
        self.interior = interior
        
        self.customMaterials = []
        self.rooms = []