
DEFAULT_MATERIALS = [
    Material('l', 'lava'), 
    Material('w','water'), 
    Material('s', 'stone'),
    Material('g', 'grass'),
    Material('d', 'dirt'),
    Material('v', 'void')
    ]


class Material(object):
    """Defines a material as a struct."""
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"(<MAT>: ({self.name}, '{self.id})')"