from flask import Flask, session, redirect, url_for, flash, request
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from project import app
from project.models.Student import Student
from project.models.Subjects import Subjects
from project.models.Meetings import Meetings
from project.models.Tutor import Tutor
from project.models.University import University
from project import db

@app.route('/')
def index():
    return render_template("start.html")

class FormLogin(FlaskForm):
    username = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

@app.route('/login/', methods=["GET", "POST"])
def login():
    login_form = FormLogin()
    if login_form.validate_on_submit():
        user_email = Student.query.filter_by(email=login_form.username.data).first()
        if user_email:
            session['email'] = user_email.email
            session['student_id'] = user_email.student_id
            session['logged'] = True
            session['name'] = user_email.name
            session['surname'] = user_email.surname
            session['study_course'] = user_email.study_course
            session['university'] = user_email.university
            flash('Login successful')
            return redirect(url_for('index'))

    return render_template('login.html', logform=login_form)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('start.html'))

if __name__ == '__main__':
    app.run(debug=True)