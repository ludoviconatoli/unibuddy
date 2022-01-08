import datetime

from project import db
from project.models.Tutor import Tutor
from project.models.Student import Student
from project.models.Meetings import Meetings
from project.models.Subjects import Subjects
from project.models.University import University
from project.models.Post import Post
from project.models.Ratings import Ratings

db.create_all()

uni1 = University("Politecnico di Torino")

db.session.add(uni1)
db.session.commit()

subject_eco = Subjects("05OIYPH", "Politecnico di Torino", "Management Engineering", "Economics", "Anna D'Ambrosio")
subject_is = Subjects("02PDWPH", "Politecnico di Torino", "Management Engineering", "Information Systems", "Claudio Giovanni Demartini")
subject_a = Subjects("16ACFPL", "Politecnico di Torino", "Ingegneria Gestionale", "Analisi I", "Silvio Mercadante")

uni1.subjects = [subject_eco, subject_is, subject_a]

db.session.add(subject_eco)
db.session.commit()
db.session.add(subject_is)
db.session.commit()
db.session.add(subject_a)
db.session.commit()

stud1 = Student("s302572@studenti.polito.it", "Pippo9!", "s302572", "Ludovico", "Natoli", "Management Engineering", "Politecnico di Torino")
stud2 = Student("s295977@studenti.polito.it", "Pluto9!", "s295977", "Michele", "Chiantera", "Management Engineering", "Politecnico di Torino")
stud3 = Student("s302249@studenti.polito.it", "Rossi9!", "s302249", "Davide", "Decurti", "Management Engineering", "Politecnico di Torino")

stud1.subjects = [subject_eco, subject_is]
stud2.subjects = [subject_eco]
stud3.subjects = [subject_is]

db.session.add(stud1)
db.session.commit()
db.session.add(stud2)
db.session.commit()
db.session.add(stud3)
db.session.commit()

meet1 = Meetings("Politecnico di Torino", "Management Engineering", "02PDWPH", "", "s302249@studenti.polito.it", 10, 1, datetime.date(2022, 1, 10), datetime.time(16, 30))
meet1.students = [stud3]
meet2 = Meetings("Politecnico di Torino", "Management Engineering", "05OIYPH", "", "s302572@studenti.polito.it", 5, 3, datetime.date(2022, 1, 12), datetime.time(14,30))
meet2.students=[stud1, stud2, stud3]

db.session.add(meet1)
db.session.commit()
db.session.add(meet2)
db.session.commit()


post1 = Post("s302572@studenti.polito.it", 2, "studiate")
db.session.add(post1)
db.session.commit()

tutor1 = Tutor("s295977@studenti.polito.it", "s295977", "Michele", "Chiantera", "Politecnico di Torino")
tutor1.subjects = [subject_a]

db.session.add(tutor1)
db.session.commit()

courses = Post.query.all()
print(courses)
