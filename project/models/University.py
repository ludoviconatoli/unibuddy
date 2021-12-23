from project import db

subjects = db.Table("university_subjects",
    db.Column("university", db.String(50), db.ForeignKey("universities.name"), primary_key=True),
    db.Column("subjects", db.String(10), db.ForeignKey("subjects.subject_id"), primary_key=True)
)

class University(db.Model):

    __tablename__ = "universities"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    students = db.relationship('Student', backref='student.university')
    tutors = db.relationship('Tutor', backref='tutor.university')
    meets = db.relationship('Meetings', backref='meetings.university')

    subjects = db.relationship("Subjects", backref="universities", lazy=True, secondary=subjects)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return ('\n ' + self.name)