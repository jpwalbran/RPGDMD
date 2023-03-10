import pytest

from RPGDMD.DMDParser import DMDParser
from RPGDMD.DMDLexer import DMDLexer
class TestDMDParser(object):

    def setup_class(self):
        self.lexer = DMDLexer()
        self.parser = DMDParser()
