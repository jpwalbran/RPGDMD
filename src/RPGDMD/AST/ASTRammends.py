class ASTRammends(object):
    
    def __init__(self, features, description=""):
        self.features = features
        self.description = description
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Ra({self.features}, {self.description})"
    