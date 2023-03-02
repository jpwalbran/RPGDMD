class Material(object):
    """Defines a material as a struct."""
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def __str__(self):
        print(f"<MAT>: ({self.name}, '{self.id})'")