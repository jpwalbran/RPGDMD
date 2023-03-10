import pytest
from RPGDMD.DMDParser import DMDParser
from RPGDMD.DMDLexer import DMDLexer
class TestDMDParser(object):

    def setup_class(self):
        self.lexer = DMDLexer()
        self.parser = DMDParser()
    
    def parse(self, command):
        tokens = self.lexer.tokenize(command)
        return self.parser.parse(tokens)
    
    

