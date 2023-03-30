class ASTRoom(object):
    def __init__(self, name, shape, mats, amendments=""):
        self.name = name
        self.shape = shape
        self.mats = mats
        self.amendments = amendments
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"ROOM({self.name}, {self.shape}, {self.mats}, {self.amendments})"