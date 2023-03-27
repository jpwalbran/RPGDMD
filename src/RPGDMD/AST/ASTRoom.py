class ASTRoom(object):
    def __init__(self, name, shape, mats, description=""):
        self.name = name
        self.shape = shape
        self.mats = mats
        self.description = description
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"R({self.name}, {self.shape}, {self.mats}, {self.description})"