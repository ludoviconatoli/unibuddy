from flask import Flask, session, redirect, url_for
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from project import app

@app.route('/')
def index():  # put application's code here
    return render_template("start.html")

class FormLogin(FlaskForm):
    username = StringField("email", validators=[DataRequired()])
    password = PasswordField("password")
    submit = SubmitField("Submit")

@app.route('/login/', methods=["GET", "POST"])
def login():
    user = False
    password = False
    form = FormLogin()

    if form.validate_on_submit():
        session["username"] = form.username.data
        session["password"] = form.password.data

        form.username.data = ""
        form.password.data = ""

        return redirect(url_for("index"))

    return render_template("login.html", login_form=form, username=user, password=password)


if __name__ == '__main__':
    app.run(debug=True)