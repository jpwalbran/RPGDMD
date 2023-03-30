from more_itertools import collapse
from sly import Parser
from RPGDMD.DMDLexer import DMDLexer
from RPGDMD.AST import *
import pprint


class DMDParser(Parser):

    #Sets the builtin debug file output
    #debugfile = 'parser.out'
    start = 'ts'

    tokens = DMDLexer.tokens

    @_('matdeflist s')
    def ts(self, p):
        return [p.matdeflist, p.s]

    @_('s')
    def ts(self, p):
        return p.s

    @_('matdeflist matdef')
    def matdeflist(self, p):
        return [p.matdeflist, p.matdef]

    @_('matdef')
    def matdeflist(self, p):
        return p.matdef

    @_('MATDEF STRING MATERIALID')
    def matdef(self, p):
        return ASTMaterial(p.STRING, p.MATERIALID)

    @_('fs s')
    def s(self, p):
        return [p.fs, p.s]

    @_('fs')
    def s(self, p):
        return p.fs

    @_('fs f')
    def fs(self, p):
        return [p.fs, p.f]

    @_('f')
    def fs(self, p):
        return p.f

    @_('NAME LPAREN sopt RPAREN LPAREN MATERIALID MATERIALID RPAREN LCBRACE fi RCBRACE')
    def f(self, p):
        return ASTFloor(p.NAME, [p.MATERIALID0, p.MATERIALID1], p.sopt, p.fi)

    @_('fi rdef')
    def fi(self, p):
        return [p.fi, p.rdef]

    @_('fi NAME DESCROP rammends')
    def fi(self, p):
        return [p.fi, ASTRint(p.NAME, p.rammends)]

    @_('rdef')
    def fi(self, p):
        return p.rdef

    @_('NAME DESCROP rammends')
    def fi(self, p):
        return ASTRint(p.NAME, p.rammends)

    @_('empty')
    def fi(self, p):
        pass

    @_('r')
    def rdef(self, p):
        return p.r

    @_('r DESCROP rammends')
    def rdef(self, p):
        p.r.amendments = p.rammends
        return p.r

    @_('LSBRACE MATERIALID MATERIALID RSBRACE sopt')
    def r(self, p):
        return [p.MATERIALID0, p.MATERIALID1, p.sopt]

    @_('NAME EQ LSBRACE MATERIALID MATERIALID RSBRACE sopt')
    def r(self, p):
        return ASTRoom(p.NAME, p.sopt, [p.MATERIALID0, p.MATERIALID1])

    @_('featurelist DESCROP descr')
    def rammends(self, p):
        return ASTRammends(p.featurelist, p.descr)

    @_('featurelist')
    def rammends(self, p):
        return ASTRammends(p.featurelist)

    @_('ft')
    def rammends(self, p):
        return ASTRammends(p.ft)

    @_('ft DESCROP descr')
    def rammends(self, p):
        return ASTRammends(p.ft, p.descr)

    @_('descr')
    def rammends(self, p):
        return ASTRammends(None, description=p.descr)

    @_('LNGBRACE fl RNGBRACE')
    def featurelist(self, p):
        return p.fl

    @_('fl ft')
    def fl(self, p):
        return [p.fl, p.ft]

    @_('ft')
    def fl(self, p):
        return p.ft

    @_('LPAREN feature RPAREN')
    def ft(self, p):
        return p.feature

    @_('LPAREN feature DESCROP descr RPAREN')
    def ft(self, p):
        p.feature.description = p.descr
        return p.feature

    @_('"D" paramlist')
    def feature(self, p):
        return ASTDoor(p.paramlist)

    @_('MATERIALID sopt')
    def feature(self, p):
        return ASTFeature(p.MATERIALID, p.sopt)

    @_('sopt')
    def feature(self, p):
        return ASTFeature("", p.sopt)

    @_('FEATOPT LSBRACE sopt RSBRACE')
    def feature(self, p):
        return ASTFeature(p.FEATOPT, p.sopt)

    @_('SHAPE paramlist')
    def sopt(self, p):
        return ASTShape(p.SHAPE, p.paramlist)

    @_('STRING')
    def descr(self, p):
        return p.STRING

    @_('MULTILINESTRING')
    def descr(self, p):
        return p.MULTILINESTRING

    @_('LSBRACE pl RSBRACE')
    def paramlist(self, p):
        return list(collapse(p.pl))

    @_('pl param')
    def pl(self, p):
        return list(collapse([p.pl, p.param]))

    @_('param')
    def pl(self, p):
        return p.param

    @_('MODEPARAM STRING')
    def param(self, p):
        return [p.MODEPARAM, p.STRING]

    @_('expr')
    def param(self, p):
        return p.expr

    @_('term')
    def expr(self, p):
        return p.term

    @_('expr PLUS term')
    def expr(self, p):
        return ASTBinOP('+', p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return ASTBinOP('-', p.expr, p.term)

    @_('exp')
    def term(self, p):
        return p.exp

    @_('term TIMES exp')
    def term(self, p):
        return ASTBinOP('*', p.term, p.exp)

    @_('term DIV exp')
    def term(self, p):
        return ASTBinOP('/', p.term, p.exp)

    @_('exp EXP factor')
    def exp(self, p):
        return ASTBinOP('^', p.exp, p.factor)

    @_('factor')
    def exp(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('MINUS factor')
    def factor(self, p):
        return ASTBinOP('-', p.factor)

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
    # with open("testCases/exampleIn.txt") as f:
    #    data = f.read()
    data = """
        matdef "Goop" 'g'
        matdef "Hammers" 'h'
        matdef "HairSpray" 'x'

        TestFloor (R[0 0 30 30])('s' 's') {
	        # Make an entryway with a puddle of goop in the middle.
	        r1 = [. .]R[15 0 5 10 m:"c"]//"A small stone entryway with a puddle of green goop in the middle of the floor."
	        r1//<('g'C[3 * w / 4 h / 2 2]//"A small circular puddle of green goop.") ('g'C[w / 4 2 * h / 3 1]//"A small circular puddle of green goop.")>
	
	        r2 = [. .]R[10 0 15 15]//\"\"\" 
		        A room that tests the multiline string literals.
		        This is mostly to have a test source for regex building.
		        \"\"\"
        }

        TestFloor2 (C[0 0 15])('s' 's') {
	        # Make another area
	        r2 = [. .]R[20 0 5 10]//"A small circular room in the floor."
        }
        
        TestFloor3 (R[0 0 30 30])('s' 's') {
            # Make an entryway with a puddle of goop in the middle.
	        r1 = [. .]R[15 0 5 10 m:"c"]//"A small stone entryway with a puddle of green goop in the middle of the floor."
	        r1//<('g'C[3 * w / 4 h / 2 2]//"A small circular puddle of green goop.") ('g'C[w / 4 2 * h / 3 1]//"A small circular puddle of green goop.")>
        }
        """

    output = parser.parse(lexer.tokenize(data))

    ol = collapse(output)
    for i in ol:
        print(type(i))
        print(i)
        if isinstance(i, ASTFloor):
            for j in collapse(i.interior):
                print(type(j))
                print(j)
