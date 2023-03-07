from sly import Parser
from DMDLexer import DMDLexer
from Material import Material


class DMDParser(Parser):

    debugfile = 'parser.out'
    start = 'ts'

    # Include a list of always given materials
    DEFAULT_MATERIALS = [
        Material('l', 'lava'), 
        Material('w','water'), 
        Material('s', 'stone'), 
        Material('g', 'grass'),
        Material('d', 'dirt'),
        Material('v', 'void')
        ]

    # Get the token list from the Lexer
    tokens = DMDLexer.tokens

    def __init__(self):
        # Run a list of materials defined in the file
        self.new_materials = []

        # Keeps a list of floors, each containing rooms
        self.floors = {}

    @_('s')
    def ts(self, p):
        return p.s
    
    # Parse material definitions
    @_('matdeflist s')
    def ts(self, p):
        return (p.matdeflist, p.s)
    
    @_('matdeflist matdef')
    def matdeflist(self, p):
        self.new_materials.append(p.matdef)
        return p.matdeflist, p.matdef 
    
    @_('matdef')
    def matdeflist(self, p):
        return p.matdef
    
    @_('MATDEF STRING MATERIALID')
    def matdef(self, p):
        return Material(p.STRING, p.MATERIALID)
    
    # Defines the options for the overall file structure
    @_('s fs')
    def s(self, p):
        return (p.fs, p.s)
    
    @_('fs')
    def s(self, p):
        return p.fs

    @_('fs f')
    def fs(self, p):
        return (p.fs, p.f)
        
    @_('f')
    def fs(self, p):
        return p.f
    
    @_('NAME "(" sopt ")" "(" MATERIALID MATERIALID ")" "{" fi "}" ')
    def f(self, p):
        return (p.NAME, p.sopt, p.MATERIALID0, p.MATERIALID1, p.fi)
    
    @_('fi rdef')
    def fi(self, p):
        return (p.fi, p.rdef)
    
    @_('fi NAME DESCROP rammends')
    def fi(self, p):
        return (p.fi, p.NAME, p.rammends)
    
    @_('rdef')
    def fi(self, p):
        return p.rdef
    
    @_('NAME DESCROP rammends')
    def fi(self, p):
        return (p.NAME, p.rammends)

    @_('r')
    def rdef(self, p):
        return p.r
    
    @_('r DESCROP rammends')
    def rdef(self, p):
        return (p.r, p.rammends)

    @_('"[" MATERIALID MATERIALID "]" sopt')
    def r(self, p):
        return (p.MATERIALID0, p.MATERIALID1, p.sopt)
    
    @_('featurelist DESCROP descr')
    def rammends(self, p):
        return (p.featurelist, p.descr)
    
    @_('featurelist')
    def rammends(self, p):
        return p.featurelist
    
    @_('descr')
    def rammends(self, p):
        return p.descr
    
    @_('"<" fl ">"')
    def featurelist(self, p):
        return p.fl
    
    @_('fl feature')
    def fl(self, p):
        return (p.fl, p.feature)
    
    @_('feature')
    def fl(self, p):
        return p.feature
    
    @_('"D" paramlist')
    def feature(self, p):
        return ("D", p.paramlist)
    
    @_('MATERIALID "(" sopt ")"')
    def feature(self, p):
        return (p.MATERIALID, p.sopt)
    
    @_('sopt')
    def feature(self, p):
        return p.sopt
    
    @_('FEATOPT "[" sopt "]"')
    def feature(self, p):
        return (p.FEATOPT, p.sopt)
    
    @_('SHAPE paramlist')
    def sopt(self, p):
        return (p.SHAPE, p.paramlist)
    
    @_('STRING')
    def descr(self, p):
        return p.STRING
    
    @_('MULTILINESTRING')
    def descr(self, p):
        return p.MULTILINESTRING

    @_('"[" pl "]"')
    def paramlist(self, p):
        return p.pl
    
    @_('pl param')
    def pl(self, p):
        return (p.pl, p.param)
    
    @_('param')
    def pl(self, p):
        return p.param
    
    @_('MODEPARAM MODE')
    def param(self, p):
        return (p.MODEPARAM, p.MODE)
    
    @_('expr')
    def param(self, p):
        return p.expr
    
    @_('term')
    def expr(self, p):
        return p.term
    
    @_('expr "+" term')
    def expr(self, p):
        return ('+' ,p.expr, p.term)
    
    @_('expr "-" term')
    def expr(self, p):
        return ('-', p.expr, p.term)
    
    @_('factor')
    def term(self, p):
        return p.factor
    
    @_('term "*" factor')
    def term(self, p):
        return ('*', p.term, p.factor)
    
    @_('term "/" factor')
    def term(self, p):
        return ('/', p.term , p.factor)
    
    @_('"(" expr ")"')
    def factor(self, p):
        return p.expr

    @_('"-" factor')
    def factor(self, p):
        return ('-', p.factor)
    
    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER
    
    @_('"w"')
    def factor(self, p):
        return "w"
    
    @_('"h"')
    def factor(self, p):
        return "h"
    
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} on line {p.lineno}")
            self.errok()
        else:
            print("Unexpected EOF encountered.")

    

if __name__ == "__main__":
    lexer = DMDLexer()
    parser = DMDParser()
    with open("exampleIn.txt") as f:
        data = "".join([x for x in f.readlines()])
    #print(data)
    parser.parse(lexer.tokenize(data))