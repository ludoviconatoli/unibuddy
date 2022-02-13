from flask import Blueprint, session, redirect, url_for, flash, render_template

from project.models.Student import Student
from project.models.Tutor import Tutor
from project.users.forms import FormLogin, FormLogout

users = Blueprint('users', __name__)

@users.route('/login/', methods=["GET", "POST"])
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
                session['tutor'] = user_tutor.email
            return redirect(url_for('main.index'))
        else:
            flash('Login error')

    return render_template('login.html', logform=login_form)

@users.route('/logout/', methods=["GET", "POST"])
def logout():
    logout_form = FormLogout()
    if logout_form.validate_on_submit():
        session.clear()
        return redirect(url_for('main.index'))

    return render_template('login.html', logform=logout_form)