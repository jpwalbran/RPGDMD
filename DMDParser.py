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
    
    # Parse material definitions
    @_('matdeflist s')
    def ts(self, p):
        return (p.matdeflist, p.s)
    
    @_('s')
    def ts(self, p):
        return p.s
    
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
    @_('fs s')
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
    
    @_('NAME LPAREN sopt RPAREN LPAREN MATERIALID MATERIALID RPAREN LCBRACE fi RCBRACE')
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

    @_('LSBRACE MATERIALID MATERIALID RSBRACE sopt')
    def r(self, p):
        return (p.MATERIALID0, p.MATERIALID1, p.sopt)
    
    @_('NAME EQ LSBRACE MATERIALID MATERIALID RSBRACE sopt')
    def r(self, p):
        return (p.NAME, p.MATERIALID0, p.MATERIALID1, p.sopt)
    
    @_('featurelist DESCROP descr')
    def rammends(self, p):
        return (p.featurelist, p.descr)
    
    @_('featurelist')
    def rammends(self, p):
        return p.featurelist
    
    @_('descr')
    def rammends(self, p):
        return p.descr
    
    @_('LNGBRACE fl RNGBRACE')
    def featurelist(self, p):
        return p.fl
    
    @_('fl ft')
    def fl(self, p):
        return (p.fl, p.ft)
    
    @_('ft')
    def fl(self, p):
        return p.ft
    
    @_('LPAREN feature RPAREN')
    def ft(self, p):
        return p.feature
    
    @_('"D" paramlist')
    def feature(self, p):
        return ("D", p.paramlist)
    
    @_('MATERIALID LPAREN sopt RPAREN')
    def feature(self, p):
        return (p.MATERIALID, p.sopt)
    
    @_('sopt')
    def feature(self, p):
        return p.sopt
    
    @_('FEATOPT LSBRACE sopt RSBRACE')
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

    @_('LSBRACE pl RSBRACE')
    def paramlist(self, p):
        return p.pl
    
    @_('pl param')
    def pl(self, p):
        return (p.pl, p.param)
    
    @_('param')
    def pl(self, p):
        return p.param
    
    @_('MODEPARAM STRING')
    def param(self, p):
        return (p.MODEPARAM, p.STRING)
    
    @_('expr')
    def param(self, p):
        return p.expr
    
    @_('term')
    def expr(self, p):
        return p.term
    
    @_('expr PLUS term')
    def expr(self, p):
        return ('+' ,p.expr, p.term)
    
    @_('expr MINUS term')
    def expr(self, p):
        return ('-', p.expr, p.term)
    
    @_('factor')
    def term(self, p):
        return p.factor
    
    @_('term TIMES factor')
    def term(self, p):
        return ('*', p.term, p.factor)
    
    @_('term DIV factor')
    def term(self, p):
        return ('/', p.term , p.factor)
    
    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('MINUS factor')
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
            print(f"Syntax error at token {p.type} on line {p.lineno} at index {p.index}")
            self.errok()
        else:
            print("Unexpected EOF encountered.")

if __name__ == "__main__":
    lexer = DMDLexer()
    parser = DMDParser()
    with open("exampleIn.txt") as f:
        data = f.read()
    output = parser.parse(lexer.tokenize(data))
    print(output)