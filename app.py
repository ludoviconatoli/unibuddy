from datetime import date, datetime

from flask import Flask, session, redirect, url_for, flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateField, TimeField, \
    SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from project import app
from project.models.Student import Student
from project.models.Subjects import Subjects
from project.models.Meetings import Meetings
from project.models.Tutor import Tutor
from project.models.University import University
from project.models.Post import Post
from project import db

from flask_mail import Message
from project import mail

@app.route('/')
def index():
    return render_template("start.html")

class FormLogin(FlaskForm):
    username = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class FormLogout(FlaskForm):
    submit = SubmitField("Logout")

class FormJoin(FlaskForm):
    chat = TextAreaField("chat", validators=[DataRequired()])
    submit = SubmitField("Post")

class FormCreate(FlaskForm):

    subject = SelectField("subject", choices=[], validators=[DataRequired()])
    email_tutor = StringField("email_tutor")
    max_members = IntegerField("max_members", validators=[DataRequired()])
    date = DateField("date", format='%Y-%m-%d', validators=[DataRequired()])
    hour = TimeField("hour", format='%H:%M', validators=[DataRequired()])
    submit = SubmitField("create")

    def validate_date(self, date):
        today=datetime.today()
        if date.data < today.date():
            raise ValidationError('The date must be in the future')


@app.route('/login/', methods=["GET", "POST"])
def login():
    login_form = FormLogin()
    if login_form.validate_on_submit():
        user_email = Student.query.filter_by(email=login_form.username.data).first()
        user_tutor = Tutor.query.filter_by(email=login_form.username.data).first()
        if user_email and user_email.password == login_form.password.data:
            session['email'] = user_email.email
            session['student_id'] = user_email.student_id
            session['logged'] = True
            session['name'] = user_email.name
            session['surname'] = user_email.surname
            session['study_course'] = user_email.study_course
            session['university'] = user_email.university
            if user_tutor:
                session['tutor'] = user_tutor
            return redirect(url_for('index'))
        else:
            flash('Login error')

    return render_template('login.html', logform=login_form)

@app.route('/logout/', methods=["GET", "POST"])
def logout():
    logout_form = FormLogout()
    if logout_form.validate_on_submit():
        session.clear()
        return redirect(url_for('index'))

    return render_template('login.html', logform=logout_form)

@app.route('/groups/')
def groups():
    meet = Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course'))
    subject=[]
    for i in meet:
        subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'), study_course=session.get('study_course'))

    if session.get('tutor'):
        subject_tutor = Tutor.query.filter_by(email=session.get('email'))
        for i in subject_tutor:
            for k in Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course'), subject_id=i.subject_id):
                meet.append(k)
                subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'), study_course=session.get('study_course'))

    today = date.today()

    return render_template('groups.html', meet=meet, subject=subject, today=today)

@app.route('/groups/<int:id>/', methods=["GET", "POST"])
def join(id):
    group = Meetings.query.filter_by(id=id).first()

    user = Student.query.filter_by(email=session.get('email')).first()

    for i in group.students:
        if i.email == session.get('email'):
            flash('You are already in this group')
            return redirect(url_for('groups'))

    group.students.append(user)
    db.session.commit()
    group.num_participants += 1
    db.session.commit()

    group = Meetings.query.filter_by(id=id).first()
    subject = Subjects.query.filter_by(subject_id=group.subject_id, university=session.get('university'),
                                       study_course=session.get('study_course')).first()

    return redirect(url_for('select', id=group.id))

@app.route('/mygroups/')
def mygroups():
    meet = Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course'))
    user = Student.query.filter_by(email=session.get('email')).first()
    subject = []
    mymeets = []

    for i in meet:
        for k in i.students:
            if k.email == session.get('email'):
                subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))
                mymeets.append(i)

    if session.get('tutor'):
        subject_tutor = Tutor.query.filter_by(email=session.get('email'))
        for i in subject_tutor:
            for k in Meetings.query.filter_by(university=session.get('university'),
                                              study_course=session.get('study_course'), subject_id=i.subject_id):
                if k.email_tutor == session.get('email'):
                    mymeets.append(k)
                    subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'),
                                                    study_course=session.get('study_course'))

    today = date.today()
    return render_template('mygroups.html', mymeets=mymeets, subject=subject, today=today)

@app.route('/mygroups/<int:id>', methods=["GET", "POST"])
def select(id):
    group = Meetings.query.filter_by(id=id).first()
    subject = Subjects.query.filter_by(
        subject_id=group.subject_id, university=session.get('university'), study_course=session.get('study_course')).first()

    user = Student.query.filter_by(email=session.get('email')).first()
    jform = FormJoin()

    if jform.validate_on_submit():
        p = Post(author=user.email, meetings_id=group.id, text=jform.chat.data)
        db.session.add(p)
        db.session.commit()

    posts = Post.query.filter_by(meetings_id=group.id)
    return render_template('select.html', group=group, jform=jform, subject=subject, posts=posts)

@app.route('/abandon/<int:id>/')
def abandon(id):
    group = Meetings.query.filter_by(id=id).first()
    user = Student.query.filter_by(email=session.get('email')).first()

    group.num_participants -= 1
    db.session.commit()
    group.students.remove(user)
    db.session.commit()

    return redirect(url_for('mygroups'))

@app.route('/create/', methods=["GET", "POST"])
def create():
    list_subjects=[]
    if session.get('tutor'):
        subject_tutor = Tutor.query.filter_by(email=session.get('email'))
        for i in subject_tutor:
            list_subjects.append(Subjects.query.filter_by(university=session.get('university'), subject_id=i.subject_id).first())

        for k in Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
           list_subjects.append(k)
    else:
        for i in Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
            list_subjects.append(i)

    cform = FormCreate()
    cform.subject.choices = list_subjects
    if cform.validate_on_submit():
        if cform.email_tutor.data:
            if Tutor.query.filter_by(email=cform.email_tutor.data).first():
                if session.get('tutor') and session.get('tutor') == cform.email_tutor.data:
                    sub = Subjects.query.filter_by(university=session.get('university'),
                                                   study_course=session.get('study_course'),
                                                   subject=cform.subject.data).first()
                    meet = Meetings(university=session.get('university'), study_course=session.get('study_course'),
                                    subject_id=sub.subject_id, email_tutor=cform.email_tutor.data,
                                    email_headgroup=session.get('email'),
                                    max_members=cform.max_members.data, num_participants=1, date=cform.date.data,
                                    hour=cform.hour.data)

                    db.session.add(meet)
                    db.session.commit()

                    user = Student.query.filter_by(email=session.get('email')).first()
                    meet.students.append(user)
                    db.session.commit()
                    return redirect(url_for('mygroups'))
                else:
                    sub = Subjects.query.filter_by(university=session.get('university'),
                                                   study_course=session.get('study_course'),
                                                   subject=cform.subject.data).first()
                    meet = Meetings(university=session.get('university'), study_course=session.get('study_course'),
                                    subject_id=sub.subject_id, email_tutor=cform.email_tutor.data,
                                    email_headgroup=session.get('email'),
                                    max_members=cform.max_members.data, num_participants=1, date=cform.date.data,
                                    hour=cform.hour.data)

                    db.session.add(meet)
                    db.session.commit()

                    user = Student.query.filter_by(email=session.get('email')).first()
                    meet.students.append(user)
                    db.session.commit()
                    send_email(cform.email_tutor.data, meet.id)

                    return redirect(url_for('mygroups'))
            else:
                flash('The student inserted is not a tutor')
                return redirect(url_for('create'))
        else:
            sub = Subjects.query.filter_by(university=session.get('university'),
                                           study_course=session.get('study_course'),
                                           subject=cform.subject.data).first()
            meet = Meetings(university=session.get('university'), study_course=session.get('study_course'),
                            subject_id=sub.getSubjectId(),
                            email_tutor="", email_headgroup=session.get('email'),
                            max_members=cform.max_members.data,
                            num_participants=1, date=cform.date.data, hour=cform.hour.data)

            db.session.add(meet)
            db.session.commit()

            user = Student.query.filter_by(email=session.get('email')).first()
            meet.students.append(user)
            db.session.commit()
            return redirect(url_for('mygroups'))

    return render_template('create.html', cform=cform)

#@app.route("/email/<string:email>")
def send_email(email, id):
    msg = Message('Unibuddy Account -- Request of tutor', sender='unibuddywebsite@gmail.com', recipients=[email])
    msg.body('Hi we are the team of Unibuddy and we are inviting you to join the meeting with id: ' + id +
             '\nPlease go to the website if you are available and join the group. \n\n Have a nice day \n\n Unibuddy')
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)