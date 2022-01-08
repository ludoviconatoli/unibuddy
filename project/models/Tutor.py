from project import db

subjects = db.Table("tutor_subjects",
    db.Column("tutor_email", db.String(50), db.ForeignKey("tutor.email"), primary_key=True),
    db.Column("subject_id", db.String(10), db.ForeignKey("subjects.subject_id"), primary_key=True)
)

class Tutor(db.Model):

    __tablename__ = "tutor"

    email = db.Column(db.String(50), primary_key=True)
    tutor_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    university = db.Column(db.String(50), db.ForeignKey("universities.name"))

    meetings = db.relationship('Meetings', backref='meetings.email_tutor')
    subjects = db.relationship('Subjects', backref='tutor', lazy=True, secondary=subjects)
    ratings = db.relationship('Ratings', backref='ratings.email_tutor')

    def __init__(self, email, tutor_id, name, surname, university):
        self.email = email
        self.tutor_id = tutor_id
        self.name = name
        self.surname = surname
        self.university = university

    def __repr__(self):
        return ('\nTutor: ' + self.tutor_id + ', name: ' + self.name + ', surname: ' + self.surname + ', email: ' + self.email)

    def getEmail(self):
        if self.email:
            return self.email

    def getUniversity(self):
        if self.university:
            return self.university

    def getSubjects(self):
        s = ""
        if self.subjects:
            for i in self.subjects:
                s = s + ", " + i
            return s