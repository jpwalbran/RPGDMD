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

        self.checkToken(tokenList[1], "STRING", '"goop"')
        self.checkToken(tokenList[2], "MATERIALID", "'g'")

    def test_multiple_matdefs(self):
        tokenList = self.getTokenList("""
        matdef "goop" 'g'
        matdef "hammers" 'q'
        """)

        assert len(tokenList) == 6

        assert tokenList[0].type == "MATDEF"

        self.checkToken(tokenList[1], "STRING", '"goop"')
        self.checkToken(tokenList[2], "MATERIALID", "'g'")

        assert tokenList[3].type == "MATDEF"

        self.checkToken(tokenList[4], "STRING", '"hammers"')
        self.checkToken(tokenList[5], "MATERIALID", "'q'")

    def test_mode_parameter_statement(self):
        tokenList = self.getTokenList('m:"c"')
        assert len(tokenList) == 2

        self.checkToken(tokenList[0], "MODEPARAM", "m:")
        self.checkToken(tokenList[1], "STRING", '"c"')

    def test_single_string_literal(self):
        tokenList = self.getTokenList('"HELLO WORLD!"')

        assert len(tokenList) == 1

        self.checkToken(tokenList[0], "STRING", '"HELLO WORLD!"')

    def test_multiline_string_literal(self):
        tokenList = self.getTokenList(""" 
            \"\"\"This is a test 
            across multiple lines.\"\"\"
        """)
        assert len(tokenList) == 1

        self.checkToken(tokenList[0], "MULTILINESTRING", """\"\"\"This is a test 
            across multiple lines.\"\"\"""")

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
