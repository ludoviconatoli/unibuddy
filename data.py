from project import db
from project.models.Tutor import Tutor
from project.models.Student import Student
from project.models.Meetings import Meetings
from project.models.Subjects import Subjects
from project.models.University import University

db.create_all()

uni1 = University("Politecnico di Torino")

db.session.add(uni1)
db.session.commit()

subject_eco = Subjects("05OIYPH", "Politecnico di Torino", "Management Engineering", "Economics", "Anna D'Ambrosio")
subject_is = Subjects("02PDWPH", "Politecnico di Torino", "Management Engineering", "Information Systems", "Claudio Giovanni Demartini")

uni1.subjects = [subject_eco, subject_is]

db.session.add(subject_eco)
db.session.commit()
db.session.add(subject_is)
db.session.commit()

stud1 = Student("s302572@studenti.polito.it", "s302572", "Ludovico", "Natoli", "Management Engineering", "Politecnico di Torino")
stud2 = Student("s295977@studenti.polito.it", "s295977", "Michele", "Chiantera", "Management Engineering", "Politecnico di Torino")
stud3 = Student("s302249@studenti.polito.it", "s302249", "Davide", "Decurti", "Management Engineering", "Politecnico di Torino")

stud1.subjects = [subject_eco, subject_is]
stud2.subjects = [subject_eco]
stud3.subjects = [subject_is]

db.session.add(stud1)
db.session.commit()
db.session.add(stud2)
db.session.commit()
db.session.add(stud3)
db.session.commit()

meet1 = Meetings("Politecnico di Torino", "02PDWPH", "", "s302249@studenti.polito.it", 10, 2)
meet1.students = [stud3, stud1]

db.session.add(meet1)
db.session.commit()


courses = Student.query.filter_by(email='s302572@studenti.polito.it').first()
print courses
