class ASTBinOP(object):

    def __init__(self, mode, t1, t2=""):
        self.mode = mode
        self.t1 = t1
        self.t2 = t2
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"BINOP({self.mode}, {self.t1}, {self.t2})"