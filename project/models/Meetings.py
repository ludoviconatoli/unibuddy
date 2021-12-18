from project import db

class Meetings(db.Model):

    __tablename__ = "meetings"

    id = db.Column(db.String(10), primary_key=True, autoincrement=True)
    university = db.Column(db.String(50), db.ForeignKey('subjects.university'))
    subject_id = db.Column(db.String(10), db.ForeignKey('subjects.subject_id'))
    email_tutor = db.Column(db.String(50), db.ForeignKey('tutor.email', nullable=True))
    email_headgroup = db.Column(db.String(50), db.ForeignKey('student.email'))
    max_members = db.Column(db.Integer())


    def __init__(self, university, subject_id, email_tutor, email_headgroup, max_members):
        self.university = university
        self.subject_id = subject_id
        self.email_tutor = email_tutor
        self.email_headgroup = email_headgroup
        self.max_members = max_members

    def __repr__(self):
        return '\nGroup: ' + {self.id} + ' in ' + {self.university} + \
               ' of ' + {self.subject_id} + ', tutor: ' + {self.email_tutor}
