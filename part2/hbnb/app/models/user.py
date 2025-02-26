from basecls import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__is_admin = is_admin
        self.places = []

    def add_place(self, place):
        self.places.append(place)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if type(first_name) is not str:
            raise TypeError("User first name must be str")
        if len(first_name) > 50:
            raise ValueError("User first name max chars is 50")
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if type(last_name) is not str:
            raise TypeError("User last name must be type str")
        if len(last_name) > 50:
            raise ValueError("User last name max chars is 50")
        self._last_name = last_name

    @property
    def email(self):
        return self._email

    # TODO email validation
    @email.setter
    def email(self, email):
        self._email = email
