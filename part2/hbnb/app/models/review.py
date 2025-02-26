from basecls import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if type(text) is not str:
            raise TypeError("Review text must be a str")
        self._text = text

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if type(rating) is not int:
            raise TypeError("Rating must be an int")
        if rating not in range(1, 6):
            raise ValueError("Rating outside of range (1-5)")
        self._rating = rating

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        self._place = place

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
