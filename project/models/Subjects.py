from project import db

class Subjects(db.Model):

    __tablename__ = "subjects"

    __table_args__ = (db.UniqueConstraint("subject_id", "university", name="constraint_uni"),)

    subject_id = db.Column(db.String(10), primary_key=True)
    university = db.Column(db.String(50))
    study_course = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    teacher = db.Column(db.String(50))

    meetings_subjects = db.relationship('Meetings', backref='meetings.subjects_id')

    def __init__(self, subject_id, university, study_course, subject, teacher):
        self.subject_id = subject_id
        self.university = university
        self.study_course = study_course
        self.subject = subject
        self.teacher = teacher

    def __repr__(self):
        return (self.subject)

    def getUniversity(self):
        if self.university:
            return self.university

    def getSubjectId(self):
        if self.subject_id:
            return self.subject_id
