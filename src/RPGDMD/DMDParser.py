from sly import Parser
from RPGDMD.DMDLexer import DMDLexer
from RPGDMD.Material import Material
import pprint


class DMDParser(Parser):

    debugfile = 'parser.out'
    start = 'ts'

    DEFAULT_MATERIALS = [
        Material('l', 'lava'), 
        Material('w','water'), 
        Material('s', 'stone'), 
        Material('g', 'grass'),
        Material('d', 'dirt'),
        Material('v', 'void')
        ]

    tokens = DMDLexer.tokens

    def __init__(self):
        self.new_materials = []
        self.floors = {}
    
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
    
    @_('empty')
    def fi(self, p):
        pass

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
    
    @_('ft')
    def rammends(self, p):
        return p.ft

    @_('ft DESCROP descr')
    def rammends(self, p):
        return (p.ft, p.descr)
    
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
    
    @_('LPAREN feature DESCROP descr RPAREN')
    def ft(self, p):
        return (p.feature, p.descr)
    
    @_('"D" paramlist')
    def feature(self, p):
        return ("D", p.paramlist)
    
    @_('MATERIALID sopt')
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
    
    @_('exp')
    def term(self, p):
        return p.exp
    
    @_('term TIMES exp')
    def term(self, p):
        return ('*', p.term, p.exp)
    
    @_('term DIV exp')
    def term(self, p):
        return ('/', p.term , p.exp)
    
    @_('exp EXP factor')
    def exp(self, p):
        return ('^', p.exp, p.factor)

    @_('factor')
    def exp(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('MINUS factor')
    def factor(self, p):
        return ('-', p.factor)
    
    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER
    
    @_('WIDTH')
    def factor(self, p):
        return p.WIDTH
    
    @_('HEIGHT')
    def factor(self, p):
        return p.HEIGHT
    
    @_('')
    def empty(self, p):
        pass
    
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} on line {p.lineno}")
            self.errok()
        else:
            print("Unexpected EOF encountered.")

if __name__ == "__main__":
    lexer = DMDLexer()
    parser = DMDParser()
    pp = pprint.PrettyPrinter(indent=2)
    #with open("testCases/exampleIn.txt") as f:
    #    data = f.read()
    data = """
        matdef "goop" 'g'
        matdef "hammers" 'q'
    """
    output = parser.parse(lexer.tokenize(data))
    pp.pprint(output)