from basecls import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if len(name) > 50:
            raise ValueError("Amenity name is too long")
        self._name = name
