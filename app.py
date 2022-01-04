from datetime import date

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

#bcrypt = Bcrypt(app)

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
    chat = TextAreaField("chat")
    submit = SubmitField("submit")

class FormCreate(FlaskForm):
    subject = SelectField("subject", validators=[DataRequired()])
    email_tutor = StringField("email_tutor", validators=[Email()])
    email_headgroup = StringField("email_headgroup", validators=[DataRequired(), Email()])
    max_members = IntegerField("max_members", validators=[DataRequired()])
    date = DateField("date", format='%Y-%m-%d', validators=[DataRequired()])
    hour = TimeField("hour", format='%H:%M', validators=[DataRequired()])
    submit = SubmitField("create")

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

    today = date.today()
    return render_template('mygroups.html', mymeets=mymeets, subject=subject, today=today)

@app.route('/mygroups/<int:id>', methods=["GET", "POST"])
def select(id):
    group = Meetings.query.filter_by(id=id).first()
    subject = Subjects.query.filter_by(
        subject_id = group.subject_id, university=session.get('university'), study_course=session.get('study_course')).first()

    user = Student.query.filter_by(email=session.get('email')).first()
    jform = FormJoin()

    if jform.validate_on_submit():
        post = Post(user.email, jform.chat.data)
        db.session.add(post)
        db.session.commit()
        group.posts.append(post)
        db.session.commit()

    return render_template('select.html', group=group, jform=jform, subject=subject, posts=group.posts)

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
    cform = FormCreate()

    if session.get('tutor'):
        subject_tutor = Tutor.query.filter_by(email=session.get('email'))
        subject=[]
        for i in subject_tutor:
            subject += Subjects.query.filter_by(university=session.get('university'), subject_id=i.subject_id).first()
    else:
        subject = Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course'))
    #if cform.validate_on_submit():

    return render_template('create.html', cform=cform, subject=subject)

if __name__ == '__main__':
    app.run(debug=True)