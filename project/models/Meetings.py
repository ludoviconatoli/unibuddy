from project import db

students = db.Table("meeting_students",
        db.Column("meetings_id", db.Integer, db.ForeignKey("meetings.id"), primary_key=True),
        db.Column("student_email", db.String(50), db.ForeignKey("student.email"), primary_key=True)
)

class Meetings(db.Model):

    __tablename__ = "meetings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    university = db.Column(db.String(50), db.ForeignKey('universities.name'))
    study_course = db.Column(db.String(50))
    subject_id = db.Column(db.String(10), db.ForeignKey('subjects.subject_id'))
    email_tutor = db.Column(db.String(50), db.ForeignKey('tutor.email'))
    email_headgroup = db.Column(db.String(50), db.ForeignKey('student.email'))
    max_members = db.Column(db.Integer())
    num_participants = db.Column(db.Integer())
    date = db.Column(db.Date())
    hour = db.Column(db.Time())


    students = db.relationship("Student", backref="meetings", lazy=True, secondary=students)

    def __init__(self, university, study_course, subject_id, email_tutor, email_headgroup, max_members, num_participants, date, hour):
        self.university = university
        self.study_course = study_course
        self.subject_id = subject_id
        self.email_tutor = email_tutor
        self.email_headgroup = email_headgroup
        self.max_members = max_members
        self.num_participants = num_participants
        self.date = date
        self.hour = hour

    def __repr__(self):
        return ('\nGroup: ' + str(self.id) + ' in ' + self.university + ' of ' + self.subject_id + ' subject, tutor: ' + self.email_tutor + ' in ' + str(self.date))

