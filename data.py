from project import db
from project.models.Tutor import Tutor
from project.models.Student import Student
from project.models.Meetings import Meetings
from project.models.Subjects import Subjects

db.create_all()

subject_eco = Subjects("05OIYPH", "Politecnico di Torino", "Management Engineering", "Economics", "Anna D'Ambrosio")
subject_is = Subjects("02PDWPH", "Politecnico di Torino", "Management Engineering", "Economics", "Anna D'Ambrosio")

db.session.add(subject_eco)
db.session.commit()
db.session.add(subject_is)
db.session.commit()

stud1 = Student("s302572@studenti.polito.it", "s302572", "Ludovico", "Natoli", "Management Engineering", "Politecnico di Torino")
stud2 = Student("s295977@studenti.polito.it", "s295977", "Michele", "Chiantera", "Management Engineering", "Politecnico di Torino")
stud3 = Student("s302249@studenti.polito.it", "s302249", "Davide", "Decurti", "Management Engineering", "Politecnico di Torino")

db.session.add(stud1)
db.session.commit()
db.session.add(stud2)
db.session.commit()
db.session.add(stud3)
db.session.commit()

meet1 = Meetings("Politecnico di Torino", "02PDWPH", "", "s302249", 10)

stud1.meetings = [meet1]
db.session.add(meet1)
db.session.commit()