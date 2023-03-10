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
    
    def test_floor_with_comment(self):
        command = """
            # This is a comment
            f1 (R[0 0 0 0]) ('s' 's') {}
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
    
    def test_floor_with_room_with_shape_mode(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_floor_with_room_ammendments(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
                r1//('w'C[0 0 5])
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_floor_with_room_ammendments_with_descr(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
                r1//('w'C[0 0 5])//"A small pool of water"
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_floor_with_two_rooms(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]
                r2 = ['w' 's']C[10 5 10]
            }
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_two_empty_floors(self):
        command = """
        f1 (R[0 0 30 30])('s' 's') {}
        f2 (E[10 4 10 5])('s' 'w') {}
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    
    def test_floor_with_material_definition(self):
        command = """
            matdef "goop" 'g'
            f1 (R[0 0 30 30])('l' 'l') {}
        """
        tree = self.parse(command)
        assert len(tree) > 0

    def test_floor_with_two_material_definitions(self):
        command = """
            matdef "goop" 'g'
            matdef "frog legs" 'f'
            f1 (R[0 0 30 30])('l' 'l') {}
        """
        tree = self.parse(command)
        assert len(tree) > 0
    
    def test_floor_with_expression(self):
        command = """
            f1 (R[4 + 2 3 * 4 7 / 8 4 ^ 2])('s' 's') {}
        """
        tree = self.parse(command)
        assert len(tree) > 0
