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
subject_acf = Subjects("01PEBPH", "Politecnico di Torino", "Management Engineering", "Accounting and Corporate Finance", "Elisa Ughetto")
subject_amps = Subjects("01PPOPH", "Politecnico di Torino", "Management Engineering", "Analysis and Management of Production Systems", "Giulia Bruno")
subject_ie = Subjects("04OJAPH", "Politecnico di Torino", "Management Engineering", "Industrial Economics", "Luigi Benfratello")
subject_so = Subjects("01QYQPH", "Politecnico di Torino", "Management Engineering", "Strategy and Organization", "Paolo Neirotti")
subject_bl = Subjects("03KYJPH", "Politecnico di Torino", "Management Engineering", "Business Law", "Paolo Rainelli")


uni1.subjects = [subject_eco, subject_is, subject_a, subject_acf, subject_amps, subject_bl, subject_so, subject_ie]

db.session.add(subject_eco)
db.session.commit()
db.session.add(subject_is)
db.session.commit()
db.session.add(subject_a)
db.session.commit()
db.session.add(subject_acf)
db.session.commit()
db.session.add(subject_amps)
db.session.commit()
db.session.add(subject_bl)
db.session.commit()
db.session.add(subject_so)
db.session.commit()
db.session.add(subject_ie)
db.session.commit()

stud1 = Student("s302572@studenti.polito.it", "Pippo9!", "s302572", "Ludovico", "Natoli", "Management Engineering", "Politecnico di Torino")
stud2 = Student("s295977@studenti.polito.it", "Pluto9!", "s295977", "Michele", "Chiantera", "Management Engineering", "Politecnico di Torino")
stud3 = Student("s302249@studenti.polito.it", "Rossi9!", "s302249", "Davide", "Decurti", "Management Engineering", "Politecnico di Torino")
stud4 = Student("s402202@studenti.polito.it", "Verdi9!", "s402202", "Sofia", "Santi", "Ingegneria Gestionale", "Politecnico di Torino")
stud5 = Student("s303065@studenti.polito.it", "Neri9!", "s303065", "Mattia", "Di Florio", "Management Engineering", "Politecnico di Torino")
stud6 = Student("s302901@studenti.polito.it", "Viola9!", "s302901", "Silvia", "D'Ambra", "Management Engineering", "Politecnico di Torino")
stud7 = Student("s204566@studenti.polito.it", "Bianchi9!", "s204566", "Alberto", "Gentili", "Management Engineering", "Politecnico di Torino")
stud8 = Student("s206023@studenti.polito.it", "Rose9!", "s206023", "Laura", "Cestani", "Management Engineering", "Politecnico di Torino")


stud1.subjects = [subject_eco, subject_is, subject_acf]
stud2.subjects = [subject_eco, subject_is, subject_acf]
stud3.subjects = [subject_eco, subject_is, subject_acf]
stud4.subjects = [subject_a]
stud5.subjects = [subject_eco, subject_is, subject_acf]
stud6.subjects = [subject_eco, subject_is, subject_acf]
stud7.subjects = [subject_eco, subject_is, subject_acf, subject_ie, subject_so, subject_amps, subject_bl]
stud8.subjects = [subject_eco, subject_is, subject_acf, subject_ie, subject_so, subject_amps, subject_bl]

db.session.add(stud1)
db.session.commit()
db.session.add(stud2)
db.session.commit()
db.session.add(stud3)
db.session.commit()
db.session.add(stud4)
db.session.commit()
db.session.add(stud5)
db.session.commit()
db.session.add(stud6)
db.session.commit()
db.session.add(stud7)
db.session.commit()
db.session.add(stud8)
db.session.commit()

tutor1 = Tutor("s295977@studenti.polito.it", "Pluto9!", "s295977", "Michele", "Chiantera", "Management Engineering", "Politecnico di Torino")
tutor1.subjects = [subject_a]
tutor2 = Tutor("s302249@studenti.polito.it", "Rossi9!", "s302249", "Davide", "Decurti", "Management Engineering", "Politecnico di Torino")
tutor2.subjects = [subject_a]
tutor3 = Tutor("s204566@studenti.polito.it", "Bianchi9!", "s204566", "Alberto", "Gentili", "Management Engineering", "Politecnico di Torino")
tutor3.subjects = [subject_is, subject_acf]
tutor4 = Tutor("s206023@studenti.polito.it", "Rose9!", "s206023", "Laura", "Cestani", "Management Engineering", "Politecnico di Torino")
tutor4.subjects = [subject_is]

db.session.add(tutor1)
db.session.commit()
db.session.add(tutor2)
db.session.commit()
db.session.add(tutor3)
db.session.commit()
db.session.add(tutor4)
db.session.commit()

meet1 = Meetings("Politecnico di Torino", "Management Engineering", "02PDWPH", "", "s302249@studenti.polito.it", 10, 1, datetime.date(2022, 3, 10), datetime.time(16, 30))
meet1.students = [stud3]
meet2 = Meetings("Politecnico di Torino", "Management Engineering", "05OIYPH", "", "s302572@studenti.polito.it", 5, 3, datetime.date(2022, 3, 12), datetime.time(14, 30))
meet2.students = [stud1, stud2, stud3]
meet3 = Meetings("Politecnico di Torino", "Ingegneria Gestionale", "16ACFPL", "s295977@studenti.polito.it", "s295977@studenti.polito.it", 5, 2, datetime.date(2022, 3, 4), datetime.time(14, 30))
meet3.students = [stud2, stud4]
meet4 = Meetings("Politecnico di Torino", "Management Engineering", "02PDWPH", "s204566@studenti.polito.it", "s204566@studenti.polito.it", 10, 1, datetime.date(2022, 3, 25), datetime.time(16, 30))
meet4.students = [stud7]

db.session.add(meet1)
db.session.commit()
db.session.add(meet2)
db.session.commit()
db.session.add(meet3)
db.session.commit()
db.session.add(meet4)
db.session.commit()

post1 = Post("s302572@studenti.polito.it", 2, "Hi guys")
post1.name = 'Ludovico'
post1.surname = 'Natoli'

db.session.add(post1)
db.session.commit()

post2 = Post("s302572@studenti.polito.it", 2, "See tomorrow")
post2.name = 'Ludovico'
post2.surname = 'Natoli'

db.session.add(post2)
db.session.commit()

post3 = Post("s302572@studenti.polito.it", 2, "Study")
post3.name = 'Ludovico'
post3.surname = 'Natoli'

db.session.add(post3)
db.session.commit()

post4 = Post("s302572@studenti.polito.it", 2, "Goodbye")
post4.name = 'Ludovico'
post4.surname = 'Natoli'

db.session.add(post4)
db.session.commit()

rate1 = Ratings(4, "")
rate2 = Ratings(4, "s295977@studenti.polito.it")
tutor1.average_rating = 4
rate3 = Ratings(5, "")
rate4 = Ratings(3, "s204566@studenti.polito.it")
rate5 = Ratings(5, "s204566@studenti.polito.it")
tutor3.average_rating = 4
rate6 = Ratings(5, "s206023@studenti.polito.it")
tutor4.average_rating = 5

db.session.add(rate1)
db.session.commit()
db.session.add(rate2)
db.session.commit()
db.session.add(rate3)
db.session.commit()
db.session.add(rate4)
db.session.commit()
db.session.add(rate5)
db.session.commit()
db.session.add(rate6)
db.session.commit()

unis = University.query.all()
print(unis)
