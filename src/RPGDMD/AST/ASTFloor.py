class ASTFloor(object):
    def __init__(self, name, mats, shape, interior):
        self.name = name
        self.mats = mats
        self.shape = shape
        self.interior = interior

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"F({self.name}, {self.mats}, {self.shape}, {self.interior})"