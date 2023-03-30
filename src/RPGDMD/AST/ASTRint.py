class ASTRint(object):

    def __init__(self, name, rammends):
        self.name = name
        self.rammends = rammends
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"RINT({self.name}, {self.rammends})"
    