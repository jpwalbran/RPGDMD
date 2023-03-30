import pytest
from RPGDMD.DMDLexer import DMDLexer
class TestDMDLexer(object):

    def setup_class(self):
        self.lexer = DMDLexer()

    def getTokenList(self, commandIn):
        return list(self.lexer.tokenize(commandIn))

    def checkToken(self, token, assertedType, assertedValue):
        assert token.type == assertedType
        assert token.value == assertedValue

    def test_matdef_command(self):
        tokenList = self.getTokenList('matdef "goop" \'g\'')
        assert len(tokenList) == 3

        assert tokenList[0].type == "MATDEF"

        self.checkToken(tokenList[1], "STRING", "goop")
        self.checkToken(tokenList[2], "MATERIALID", 'g')

    def test_multiple_matdefs(self):
        tokenList = self.getTokenList("""
        matdef "goop" 'g'
        matdef "hammers" 'q'
        """)

        assert len(tokenList) == 6

        assert tokenList[0].type == "MATDEF"

        self.checkToken(tokenList[1], "STRING", "goop")
        self.checkToken(tokenList[2], "MATERIALID", 'g')

        assert tokenList[3].type == "MATDEF"

        self.checkToken(tokenList[4], "STRING", "hammers")
        self.checkToken(tokenList[5], "MATERIALID", 'q')

    def test_mode_parameter_statement(self):
        tokenList = self.getTokenList('m:"c"')
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "MODEPARAM", "m:")
        self.checkToken(tokenList[1], "STRING", 'c')

    def test_single_string_literal(self):
        tokenList = self.getTokenList('"HELLO WORLD!"')

        assert len(tokenList) == 1

        self.checkToken(tokenList[0], "STRING", "HELLO WORLD!")

    def test_multiline_string_literal(self):
        tokenList = self.getTokenList(""" 
            \"\"\"This is a test 
            across multiple lines.\"\"\"
        """)
        assert len(tokenList) == 1

        self.checkToken(tokenList[0], "MULTILINESTRING", """This is a test 
            across multiple lines.""")

    def test_illegal_character(self):
        tokenList = self.getTokenList(":")
        assert len(tokenList) == 0

    def test_number_casting(self):
        tokenList = self.getTokenList("10")

        assert len(tokenList) == 1
        self.checkToken(tokenList[0], "NUMBER", 10)


    def test_paren_matching(self):
        tokenList = self.getTokenList("()")
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "LPAREN", "(")
        self.checkToken(tokenList[1], "RPAREN", ")")

    def test_curly_bracket_matching(self):
        tokenList = self.getTokenList("{}")
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "LCBRACE", "{")
        self.checkToken(tokenList[1], "RCBRACE", "}")

    def test_angle_bracket_matching(self):
        tokenList = self.getTokenList("<>")
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "LNGBRACE", "<")
        self.checkToken(tokenList[1], "RNGBRACE", ">")
    
    def test_square_bracket_matching(self):
        tokenList = self.getTokenList("[]")
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "LSBRACE", "[")
        self.checkToken(tokenList[1], "RSBRACE", "]")
    
    def test_legal_names(self):
        names = ["r1", "r2", "r3", "_Underscores_", "Apple", "Foo"]
        tokenList = self.getTokenList("".join(x + " " for x in names))
        assert len(tokenList) == 6

        for i,t in enumerate(tokenList):
            self.checkToken(t, "NAME", names[i])
    
    def test_width_and_height(self):
        tokenList = self.getTokenList("w h")
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "WIDTH", "w")
        self.checkToken(tokenList[1], "HEIGHT", "h")
    
    def test_shapes(self):
        tokenList = self.getTokenList("R C E L P")
        assert len(tokenList) == 5

        for t in tokenList:
            assert t.type == "SHAPE"
    
    def test_material_id(self):
        tokenList = self.getTokenList("'g' 'w' 's' 'l'")
        assert len(tokenList) == 4

        for t in tokenList:
            assert t.type == "MATERIALID"
        
    def test_description_operator(self):
        tokenList = self.getTokenList("//")
        assert len(tokenList) == 1
        assert tokenList[0].type == "DESCROP"