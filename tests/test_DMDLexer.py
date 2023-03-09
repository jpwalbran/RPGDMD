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