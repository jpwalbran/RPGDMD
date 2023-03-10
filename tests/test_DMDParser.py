import pytest
from RPGDMD.DMDLexer import DMDLexer
from RPGDMD.DMDParser import DMDParser

class TestDMDParser(object):

    def setup_class(self):
        self.lexer = DMDLexer()
        self.parser = DMDParser()
    
    def parse(self, commandIn):
        tokenList = self.lexer.tokenize(commandIn)
        return self.parser.parse(tokenList)

    def test_single_material_definition(self):
        command = "matdef \"goop\" 'g'"
        output = self.parse(command)
        assert len(output) == 1