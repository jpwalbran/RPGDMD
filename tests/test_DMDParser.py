import pytest
from RPGDMD.DMDLexer import DMDLexer
from RPGDMD.DMDParser import DMDParser
from RPGDMD.AST import *


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
        floor = self.parse(command)
        assert type(floor) == ASTFloor

        assert floor.name == "f1"
        assert floor.mats == ['s', 's']
        s = floor.shape
        assert s.shape == "R"
        assert s.params == [0, 0, 30, 30]

    def test_single_floor_with_simple_room(self):
        command = """
            f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor
        interior = floor.interior
        assert type(interior) == ASTRoom
        assert interior.name == "r1"
        assert interior.mats == ['.', '.']
        assert interior.shape.shape == "R"
        assert interior.shape.params == [15, 0, 5, 10]

    def test_floor_with_comment(self):
        command = """
            # This is a comment
            f1 (R[0 0 0 0]) ('s' 's') {}
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor
        assert floor.name == "f1"
        assert floor.mats == ['s', 's']
        assert floor.shape.shape == "R"
        assert floor.shape.params == [0, 0, 0, 0]

    def test_single_floor_with_room_with_description(self):
        command = """
            f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]//"A test room"
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor
        interior = floor.interior
        assert type(interior) == ASTRoom
        assert interior.name == "r1"
        assert type(interior.amendments) == ASTRammends
        assert interior.amendments.features == None
        assert interior.amendments.description == "A test room"

    def test_floor_with_room_with_shape_mode(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor

        assert floor.mats == ['s','s']
        assert type(floor.shape) == ASTShape
        shape = floor.shape
        assert shape.shape == "R"
        assert shape.params == [0, 0, 30, 30]

        room = floor.interior
        assert type(room) == ASTRoom
        assert room.name == "r1"
        assert room.mats == ['.', '.']
        assert type(room.shape) == ASTShape
        rs = room.shape
        assert rs.shape == "R"
        assert rs.params == [15,0,5,10, "m:", 'c']
        assert type(room.amendments) == ASTRammends
        assert room.amendments.description == "A test room"

    def test_floor_with_room_ammendments(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
                r1//('w'C[0 0 5])
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor

        assert floor.name == "f1"
        assert floor.mats == ['s','s']
        assert type(floor.shape) == ASTShape
        shape = floor.shape
        assert shape.shape == "R"
        assert shape.params == [0,0,30,30]
        assert type(floor.interior) == list
        interior = floor.interior
        room = interior[0]
        assert type(room) == ASTRoom
        assert room.name == "r1"
        assert room.amendments.description == "A test room"

        rint = interior[1]
        assert type(rint) == ASTRint
        assert rint.name == "r1"
        assert type(rint.rammends) == ASTRammends
        ramds = rint.rammends
        assert type(ramds.features) == ASTFeature
        feat = ramds.features
        assert feat.mat == "w"
        assert type(feat.shape) == ASTShape

    def test_floor_with_room_ammendments_with_descr(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
                r1//('w'C[0 0 5])//"A small pool of water"
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor

        assert floor.name == "f1"

        interior = floor.interior
        assert type(interior) == list

        room = interior[0]
        assert type(room) == ASTRoom
        assert type(room.amendments) == ASTRammends

        assert type(interior[1]) == ASTRint
        rint = interior[1]
        assert rint.name == "r1"
        assert type(rint.rammends.features) == ASTFeature
        assert rint.rammends.description == "A small pool of water"


    def test_floor_with_room_feature_list(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10 m:"c"]//"A test room"
                r1//<('w'C[0 0 5]//"A small pool of water") ('g'R[0 0 10 10])>
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor
        assert floor.name == "f1"
        assert type(floor.interior) == list
        interior = floor.interior
        assert type(interior[0]) == ASTRoom
        assert type(interior[1]) == ASTRint

        rint = interior[1]

        assert rint.name == "r1"
        assert type(rint.rammends) == ASTRammends
        ramds = rint.rammends
        assert type(ramds.features) == list
        for feat in ramds.features:
            assert type(feat) == ASTFeature


    def test_floor_with_two_rooms(self):
        command = """
        f1 (R[0 0 30 30])('s' 's'){
                r1 = [. .]R[15 0 5 10]
                r2 = ['w' 's']C[10 5 10]
            }
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor

        interior = floor.interior

        assert type(interior) == list
        assert type(interior[0]) == ASTRoom
        assert type(interior[1]) == ASTRoom

    def test_two_empty_floors(self):
        command = """
        f1 (R[0 0 30 30])('s' 's') {}
        f2 (E[10 4 10 5])('s' 'w') {}
        """
        tree = self.parse(command)
        assert type(tree) == list
        assert len(tree) == 2

        assert type(tree[0]) == ASTFloor
        assert type(tree[1]) == ASTFloor

        assert tree[0].name == "f1"
        assert tree[1].name == "f2"

    def test_floor_with_material_definition(self):
        command = """
            matdef "goop" 'g'
            f1 (R[0 0 30 30])('l' 'l') {}
        """
        tree = self.parse(command)
        assert type(tree) == list
        assert len(tree) == 2
        assert type(tree[0]) == ASTMaterial
        assert tree[0].name == "goop"
        assert tree[0].id == 'g'
        assert type(tree[1]) == ASTFloor

    def test_floor_with_two_material_definitions(self):
        command = """
            matdef "goop" 'g'
            matdef "frog legs" 'f'
            f1 (R[0 0 30 30])('l' 'l') {}
        """
        tree = self.parse(command)
        assert type(tree) == list
        assert type(tree[0]) == list

        mats = tree[0]
        assert mats[0].name == "goop"
        assert mats[0].id == 'g'
        
        assert type(mats[1]) == ASTMaterial
        assert mats[1].name == "frog legs"
        assert mats[1].id == 'f'

    def test_floor_with_simple_expressions(self):
        command = """
            f1 (R[4 + 2 3 * 4 7 / 8 4 ^ 2])('s' 's') {}
        """
        floor = self.parse(command)
        assert type(floor) == ASTFloor
        assert floor.name == "f1"
        assert floor.mats == ['s', 's']

        assert type(floor.shape) == ASTShape
        shape = floor.shape
        assert shape.shape == "R"

        for i in shape.params:
            assert type(i) == ASTBinOP

        assert shape.params[0].mode == "+"
        assert shape.params[0].t1 == 4
        assert shape.params[0].t2 == 2

        assert shape.params[1].mode == "*"
        assert shape.params[1].t1 == 3
        assert shape.params[1].t2 == 4

        assert shape.params[2].mode == "/"
        assert shape.params[2].t1 == 7
        assert shape.params[2].t2 == 8

        assert shape.params[3].mode == "^"
        assert shape.params[3].t1 == 4
        assert shape.params[3].t2 == 2