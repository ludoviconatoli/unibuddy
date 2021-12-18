from project import db

class Student(db.Model): #sottoclasse di un modello

    __tablename__ = "student"

    email = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    study_course = db.Column(db.String(30), db.ForeignKey('subjects.study_course'))
    university = db.Column(db.String(50), db.ForeignKey('subjects.university'))

    meetings = db.relationship('Meetings', backref='meetings.email_headgroup')

    def __init__(self, email, student_id, name, surname, study_course, university):
        self.email = email
        self.student_id = student_id
        self.name = name
        self.surname = surname
        self.study_course = study_course
        self.university = university

    def __repr__(self):
        return '\nStudent: ' + {self.student_id} + ', name: ' + {self.name} + ', surname: ' + {self.surname} + ', email: ' + {self.email}
