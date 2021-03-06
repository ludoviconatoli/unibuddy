from project import db

subjects = db.Table("student_subjects",
    db.Column("student_id", db.String(10), db.ForeignKey("student.student_id"), primary_key=True),
    db.Column("subject_id", db.String(10), db.ForeignKey("subjects.subject_id"), primary_key=True)
)

class Student(db.Model):

    __tablename__ = "student"

    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    student_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    study_course = db.Column(db.String(30), nullable=False)
    university = db.Column(db.String(50), db.ForeignKey('universities.name'))

    subjects = db.relationship("Subjects", backref="student", lazy=True, secondary=subjects)
    headgroups = db.relationship("Meetings", backref="meetings.email_headgroup")
    posts = db.relationship("Post", backref="post.author")

    def __init__(self, email, password, student_id, name, surname, study_course, university):
        self.email = email
        self.password = password
        self.student_id = student_id
        self.name = name
        self.surname = surname
        self.study_course = study_course
        self.university = university

    def __repr__(self):
        return ('\nStudent: ' + self.student_id + ', name: ' + self.name + ', surname: ' + self.surname + ', email: ' + self.email)

    def getEmail(self):
        if self.email:
            return self.email

    def getUniversity(self):
        if self.university:
            return self.university