class ASTFeature(object):
    def __init__(self, mat, shape, description=""):
        self.mat = mat
        self.shape = shape
        self.description = description
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"F({self.mat}, {self.shape}, {self.description})"