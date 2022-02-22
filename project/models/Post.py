from project import db

class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    author = db.Column(db.String(50), db.ForeignKey('student.email'), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    meetings_id = db.Column(db.Integer(), db.ForeignKey('meetings.id'))
    text = db.Column(db.String(260))

    def __init__(self, author, meetings_id, text):
        self.author = author
        self.meetings_id=meetings_id
        self.text = text

    def __repr__(self):
        return ('\n ' + self.text)