from project import db

class Tutor(db.Model): #sottoclasse di un modello

    __tablename__ = "tutor"

    email = db.Column(db.String(50), primary_key=True)
    subject_id = db.Column(db.String(10), db.ForeignKey('subjects.subject_id', primary_key=True))
    tutor_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    university = db.Column(db.String(50), db.ForeignKey('subjects.university'))

    meetings = db.relationship('Meetings', backref='meetings.email_tutor')

    def __init__(self, email, subject_id, tutor_id, name, surname, university):
        self.email = email
        self.subject_id = subject_id
        self.tutor_id = tutor_id
        self.name = name
        self.surname = surname
        self.university = university

    def __repr__(self):
        return '\nTutor: ' + {self.tutor_id} + ', name: ' + {self.name} + \
               ', surname: ' + {self.surname} + ', email: ' + {self.email} + ', subject: ' + {self.subject_id}
