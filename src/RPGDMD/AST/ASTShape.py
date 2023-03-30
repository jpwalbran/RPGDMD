class ASTShape(object):
    def __init__(self, shapeOpt, params):
        self.shape = shapeOpt
        self.params = params
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"{self.shape}({self.params})"