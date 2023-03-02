from sly import Parser
from DMDLexer import DMDLexer
from Material import Material


class DMDParser(Parser):
    
    # Include a list of always given materials
    DEFAULT_MATERIALS = [
        Material('l', 'lava'), 
        Material('w','water'), 
        Material('s', 'stone'), 
        Material('g', 'grass'),
        Material('d', 'dirt'),
        Material('v', 'void')
        ]

    # Get the token list from the Lexer
    tokens = DMDLexer.tokens

    def __init__(self):
        # Run a list of materials defined in the file
        self.new_materials = []

        # Keeps a list of floors, each containing rooms
        self.floors = {}

    @_('s')
    def ts(self, p):
        return p.s
    
    # Parse material definitions
    @_('matdeflist s')
    def ts(self, p):
        return (p.matdeflist, p.s)
    
    @_('matdeflist matdef')
    def matdeflist(self, p):
        self.new_materials.append(p.matdef)
        return p.matdeflist, p.matdef 
    
    @_('matdef')
    def matdeflist(self, p):
        return p.matdef
    
    @_('MATDEF STRING MATERIALID')
    def matdef(self, p):
        return Material(p.NAME, p.MATERIALID)
    
    # Defines the options for the overall file structure
    @_('fs s')
    def s(self, p):
        return (p.fs, p.s)
    
    @_('fs')
    def s(self, p):
        return p.fs
    
    @_('fs f')
    def fs(self, p):
        return (p.fs, p.f)
    
    @_('f')
    def fs(self, p):
        return p.f
    