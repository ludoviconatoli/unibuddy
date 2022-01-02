from datetime import date

from flask import Flask, session, redirect, url_for, flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from project import app
from project.models.Student import Student
from project.models.Subjects import Subjects
from project.models.Meetings import Meetings
from project.models.Tutor import Tutor
from project.models.University import University
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

@app.route('/login/', methods=["GET", "POST"])
def login():
    login_form = FormLogin()
    if login_form.validate_on_submit():
        user_email = Student.query.filter_by(email=login_form.username.data).first()
        if user_email and user_email.password == login_form.password.data:
            session['email'] = user_email.email
            session['student_id'] = user_email.student_id
            session['logged'] = True
            session['name'] = user_email.name
            session['surname'] = user_email.surname
            session['study_course'] = user_email.study_course
            session['university'] = user_email.university
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
    meet = Meetings.query.filter_by(university=session.get('university'))
    subject=[]
    for i in meet:
        subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))

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
    jform = FormJoin()

    if jform.validate_on_submit():
        return redirect(url_for())

    return render_template('join.html', group=group, jform=jform)

@app.route('/mygroups/')
def mygroups():
    meet = Meetings.query.filter_by(university=session.get('university'))
    user = Student.query.filter_by(email=session.get('email')).first()
    subject = []
    mymeets = []

    for i in meet:
        for k in i.students:
            if k.email == session.get('email'):
                subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))
                mymeets += i

    return render_template('mygroups.html', mymeets=mymeets, subject=subject)

@app.route('/mygroups/<int:id>')
def select(id):
    group = Meetings.query.filter_by(id=id).first()
    jform = FormJoin()

    return render_template('join.html', group=group, jform=jform)

if __name__ == '__main__':
    app.run(debug=True)