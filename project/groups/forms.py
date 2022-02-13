from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, StringField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email


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

class FormAdd(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Tutor')

class FormTutors(FlaskForm):
    subject = SelectField('Subject', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')