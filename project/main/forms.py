from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Email

class FormRate(FlaskForm):
    rating = RadioField('rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    submit = SubmitField("Rate")

class FormRateTutor(FlaskForm):
    rating = RadioField('rating tutor', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    email_tutor = StringField("Email Tutor", validators=[DataRequired(), Email()])
    submit = SubmitField("Rate")