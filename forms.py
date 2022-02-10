from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateField, TimeField, \
    SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from datetime import date, datetime

class FormLogin(FlaskForm):
    username = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class FormLogout(FlaskForm):
    submit = SubmitField("Logout")

class FormJoin(FlaskForm):
    chat = TextAreaField("chat", validators=[DataRequired()])
    submit = SubmitField("Post")

class FormCreate(FlaskForm):

    subject = SelectField("Subject", choices=[], validators=[DataRequired()])
    email_tutor = StringField("Email Tutor")
    max_members = IntegerField("Max members", validators=[DataRequired()])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    hour = TimeField("Hour", format='%H:%M', validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_date(self, date):
        today = datetime.today()
        if date.data < today.date():
            raise ValidationError('The date must be in the future')

    def validate_max_members(self, max_members):
        if max_members.data <= 1:
            raise ValidationError('The number of students must be higher than 1')

class FormRate(FlaskForm):
    rating = RadioField('rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    submit = SubmitField("Rate")

class FormRateTutor(FlaskForm):
    rating = RadioField('rating tutor', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    email_tutor = StringField("Email Tutor", validators=[DataRequired(), Email()])
    submit = SubmitField("Rate")

class FormAdd(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Tutor')

class FormTutors(FlaskForm):
    subject = SelectField('Subject', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')