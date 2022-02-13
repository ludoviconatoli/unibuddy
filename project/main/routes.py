from flask import Blueprint, render_template, redirect, url_for, session, flash

from project import db
from project.main.forms import FormRate, FormRateTutor
from project.models.Meetings import Meetings
from project.models.Ratings import Ratings
from project.models.Tutor import Tutor

main = Blueprint('main', __name__)

@main.route('/')
def index():
    num_groups = 0
    for i in Meetings.query.all():
        num_groups += 1

    sum = 0
    num = 0
    for i in Ratings.query.filter_by(email_tutor=""):
        sum += i.rating
        num += 1

    average = sum/num
    return render_template("start.html", num_groups=num_groups, average=average)

@main.route('/rate/', methods=["GET", "POST"])
def rate():
    rform = FormRate()

    if rform.validate_on_submit():
        rate = Ratings(rating=rform.rating.data, email_tutor="")
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('rate.html', rform=rform)

@main.route('/rate/tutor/', methods=["GET", "POST"])
def rate_tutor():
    rtform = FormRateTutor()

    if rtform.validate_on_submit():
        if Tutor.query.filter_by(email=rtform.email_tutor.data).first():
            if session.get('tutor') and session.get('email') == rtform.email_tutor.data:
                flash('You cannot rate yourself')
                return redirect(url_for('main.rate'))

            rate = Ratings(rating=rtform.rating.data, email_tutor=rtform.email_tutor.data)
            db.session.add(rate)
            db.session.commit()

            ratings = Ratings.query.filter_by(email_tutor=rtform.email_tutor.data)
            sum=0
            k=0
            for i in ratings:
                sum += i.rating
                k += 1

            tutor = Tutor.query.filter_by(email=rtform.email_tutor.data).first()
            tutor.average_rating = sum/k
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('The email inserted is not referred to a tutor')
            return redirect(url_for('main.rate'))

    return render_template('rate_tutor.html', rtform=rtform)

@main.errorhandler(404)
def error_404(error):
	return render_template('404.html')

@main.errorhandler(500)
def error_500(error):
	return render_template('500.html')
