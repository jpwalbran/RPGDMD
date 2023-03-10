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
    
    def test_single_empty_floor(self):
        command = """
            f1 (R[0 0 30 30])('s' 's') {} 
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_single_floor_with_simple_room(self):
        command = """
            f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_single_floor_with_room_with_description(self):
        command = """
            f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]//"A test room"
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0

