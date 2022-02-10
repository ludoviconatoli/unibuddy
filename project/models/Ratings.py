from project import db

class Ratings(db.Model):

    __tablename__ = "ratings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer())
    email_tutor = db.Column(db.String(50), db.ForeignKey('tutor.email'))

    def __init__(self, rating, email_tutor):
        self.rating = rating
        self.email_tutor = email_tutor