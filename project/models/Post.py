from project import db

class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    author = db.Column(db.String(50))
    text = db.Column(db.String(260))

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __repr__(self):
        return ('\ntext: ' + self.text)