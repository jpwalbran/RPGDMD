import pytest
from src.RPGDMD.DMDLexer import DMDLexer

class TestDMDLexer(object):

    def test_always_pass(self):
        self.lexer = DMDLexer()
        assert len(self.lexer.tokenize("matdef")) == 1
    