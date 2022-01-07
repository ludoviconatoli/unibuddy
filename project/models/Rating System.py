from project import db

class Ratings(db.Model):

    __tablename__ = "ratings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer())

    def __init__(self, rating):
        self.rating = rating
