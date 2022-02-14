from project import db
from project.models.Student import Student

subjects = db.Table("tutor_subjects",
    db.Column("tutor_email", db.String(50), db.ForeignKey("tutor.email"), primary_key=True),
    db.Column("subject_id", db.String(10), db.ForeignKey("subjects.subject_id"), primary_key=True)
)

class Tutor(Student):

    __tablename__ = "tutor"

    __mapper_args__ = {'concrete': True}

    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    student_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    study_course = db.Column(db.String(30), nullable=False)
    university = db.Column(db.String(50), db.ForeignKey('universities.name'))
    average_rating = db.Column(db.Float())

    meetings = db.relationship('Meetings', backref='meetings.email_tutor')
    subjects = db.relationship('Subjects', backref='tutor', lazy=True, secondary=subjects)
    ratings = db.relationship('Ratings', backref='ratings.email_tutor')

    def __init__(self, email, password, student_id, name, surname, study_course, university):
        super().__init__(email, password, student_id, name, surname, study_course, university)

    def __repr__(self):
        return ('\nTutor: ' + self.tutor_id + ', name: ' + self.name + ', surname: ' + self.surname + ', email: ' + self.email)

    def getSubjects(self):
        s = ""
        if self.subjects:
            for i in self.subjects:
                s = s + ", " + i
            return s