from project import db

students = db.Table("meeting_students",
        db.Column("meetings_id", db.Integer, db.ForeignKey("meetings.id"), primary_key=True),
        db.Column("student_email", db.String(50), db.ForeignKey("student.email"), primary_key=True)
)

class Meetings(db.Model):

    __tablename__ = "meetings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    university = db.Column(db.String(50), db.ForeignKey('universities.name'))
    subject_id = db.Column(db.String(10), db.ForeignKey('subjects.subject_id'))
    email_tutor = db.Column(db.String(50), db.ForeignKey('tutor.email'))
    email_headgroup = db.Column(db.String(50), db.ForeignKey('student.email'))
    max_members = db.Column(db.Integer())

    students = db.relationship("Student", backref="meetings", lazy=True, secondary=students)

    def __init__(self, university, subject_id, email_tutor, email_headgroup, max_members):
        self.university = university
        self.subject_id = subject_id
        self.email_tutor = email_tutor
        self.email_headgroup = email_headgroup
        self.max_members = max_members

    def __repr__(self):
        return ('\nGroup: ' + str(self.id) + ' in ' + self.university + ' of ' + self.subject_id + ' subject, tutor: ' + self.email_tutor)

