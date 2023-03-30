class ASTDoor(object):
    def __init__(self, params):
        self.params = params
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"D({self.params})"