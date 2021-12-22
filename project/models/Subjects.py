from project import db

class Subjects(db.Model):

    __tablename__ = "subjects"

    subject_id = db.Column(db.String(10), primary_key=True)
    university = db.Column(db.String(50), primary_key=True)
    study_course = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    teacher = db.Column(db.String(50))

    university_tutors = db.relationship('Tutor', backref='tutor.university')
    student_universities = db.relationship('Student', backref='student.university')
    student_study_courses = db.relationship('Student', backref='student.study_course')
    meetings_subjects = db.relationship('Meetings', backref='meetings.subjects_id')

    def __init__(self, subject_id, university, study_course, subject, teacher):
        self.subject_id = subject_id
        self.university = university
        self.study_course = study_course
        self.subject = subject
        self.teacher = teacher

    def __repr__(self):
        return '\nSubject: ' + {self.subject_id} + ' ' + {self.subject} + \
               ', teached in ' + {self.university} + ' by ' + {self.teacher}
