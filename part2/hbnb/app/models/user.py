from basecls import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:51]
        self.last_name = last_name[:51]
        self.email = email
        self.is_admin = is_admin
        self.places = []


    def add_place(self, place):
        self.places.append(place)
