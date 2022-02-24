from datetime import date

from flask import Blueprint, session, render_template, flash, redirect, url_for, request

from project import db
from project.groups.forms import FormJoin, FormCreate, FormAdd, FormTutors
from project.models.Meetings import Meetings
from project.models.Post import Post
from project.models.Student import Student
from project.models.Subjects import Subjects
from project.models.Tutor import Tutor
from project.models.University import University
from project.users.utils import send_email

meets = Blueprint('meets', __name__)

@meets.route('/groups/')
def groups():
    meet = []
    for i in Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
        meet.append(i)

    subject=[]
    for i in meet:
        subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'), study_course=session.get('study_course'))

    if session.get('tutor'):
        tutor = Tutor.query.filter_by(email=session.get('email')).first()
        for i in tutor.subjects:
            for k in Meetings.query.filter_by(university=session.get('university'), subject_id=i.subject_id):
                meet.append(k)
                subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))

    today = date.today()

    return render_template('groups.html', meet=meet, subject=subject, today=today)

@meets.route('/groups/<int:id>/', methods=["GET", "POST"])
def join(id):
    group = Meetings.query.filter_by(id=id).first()

    user = Student.query.filter_by(email=session.get('email')).first()

    for i in group.students:
        if i.email == session.get('email'):
            flash('You are already in this group')
            return redirect(url_for('meets.groups'))

    if session.get('tutor'):
        tutor = Tutor.query.filter_by(email=session.get('tutor')).first()
        if tutor:
            for i in tutor.subjects:
                if group.subject_id == i.subject_id:
                    if group.email_tutor != "":
                        flash('The group already has a tutor')
                        return redirect(url_for('meets.groups'))
                    else:
                        group.email_tutor = session.get('tutor')
                        db.session.commit()
                        group.students.append(user)
                        db.session.commit()
                        group.num_participants += 1
                        db.session.commit()
                        return redirect(url_for('meets.select', id=group.id))

    group.students.append(user)
    db.session.commit()
    group.num_participants += 1
    db.session.commit()

    group = Meetings.query.filter_by(id=id).first()

    return redirect(url_for('meets.select', id=group.id))

@meets.route('/mygroups/')
def mygroups():
    meet = []
    for i in Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
        meet.append(i)

    user = Student.query.filter_by(email=session.get('email')).first()
    subject = []
    mymeets = []

    for i in meet:
        for k in i.students:
            if k.email == session.get('email'):
                subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))
                mymeets.append(i)

    if session.get('tutor'):
        tutor = Tutor.query.filter_by(email=session.get('email')).first()
        for i in tutor.subjects:
            for k in Meetings.query.filter_by(university=session.get('university'), subject_id=i.subject_id):
                if k.email_tutor == session.get('email'):
                    mymeets.append(k)
                    subject += Subjects.query.filter_by(subject_id=i.subject_id, university=session.get('university'))

    today = date.today()
    return render_template('mygroups.html', mymeets=mymeets, subject=subject, today=today)

@meets.route('/mygroups/<int:id>', methods=["GET", "POST"])
def select(id):
    group = Meetings.query.filter_by(id=id).first()
    subject = Subjects.query.filter_by(subject_id=group.subject_id, university=session.get('university'), study_course=session.get('study_course')).first()

    user = Student.query.filter_by(email=session.get('email')).first()
    jform = FormJoin()

    if jform.validate_on_submit():
        p = Post(author=user.email, meetings_id=group.id, text=jform.chat.data)
        p.name = user.name
        p.surname = user.surname
        db.session.add(p)
        db.session.commit()


    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(meetings_id=group.id).paginate(page=page, per_page=5)

    return render_template('select.html', group=group, jform=jform, subject=subject, posts=posts)

@meets.route('/abandon/<int:id>/')
def abandon(id):
    group = Meetings.query.filter_by(id=id).first()
    user = Student.query.filter_by(email=session.get('email')).first()

    group.num_participants -= 1
    db.session.commit()
    group.students.remove(user)
    db.session.commit()

    if group.email_tutor == user.email:
        group.email_tutor = ""
        db.session.commit()

    return redirect(url_for('meets.mygroups'))

@meets.route('/delete/<int:id>')
def delete(id):
    group = Meetings.query.filter_by(id=id).first()
    db.session.delete(group)
    db.session.commit()

    return redirect(url_for('meets.mygroups'))

@meets.route('/create/', methods=["GET", "POST"])
def create(**kwargs):
    list_subjects=[]
    if session.get('tutor'):
        tutor = Tutor.query.filter_by(email=session.get('email')).first()
        for i in tutor.subjects:
            list_subjects.append(Subjects.query.filter_by(university=session.get('university'), subject_id=i.subject_id).first())

        for k in Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
           list_subjects.append(k)
    else:
        for i in Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
            list_subjects.append(i)

    cform = FormCreate()
    cform.subject.choices = list_subjects
    if cform.validate_on_submit():
        for i in Meetings.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
            for k in i.students:
                if(k.email == session.get('email') and i.date == cform.date.data and i.hour == cform.hour.data):
                    flash('You cannot create a group at the same moment in which you join another group')
                    return redirect(url_for('meets.create'))

        if cform.email_tutor.data:
            if Tutor.query.filter_by(email=cform.email_tutor.data).first():
                if session.get('tutor') and session.get('email') == cform.email_tutor.data:
                    sub = Subjects.query.filter_by(university=session.get('university'),
                                                   subject=cform.subject.data).first()
                    meet = Meetings(university=session.get('university'), study_course=sub.study_course,
                                    subject_id=sub.subject_id, email_tutor=cform.email_tutor.data,
                                    email_headgroup=session.get('email'),
                                    max_members=cform.max_members.data, num_participants=1, date=cform.date.data,
                                    hour=cform.hour.data)

                    db.session.add(meet)
                    db.session.commit()

                    user = Student.query.filter_by(email=session.get('email')).first()
                    meet.students.append(user)
                    db.session.commit()
                    return redirect(url_for('meets.mygroups'))
                else:
                    for i in Subjects.query.filter_by(study_course=session.get('study_course'),
                                                      university=session.get('university')):
                        t = Tutor.query.filter_by(email=cform.email_tutor.data).first()
                        for j in t.subjects:
                            if i.subject_id == j.subject_id:
                                sub = Subjects.query.filter_by(university=session.get('university'),
                                                               study_course=session.get('study_course'),
                                                               subject=cform.subject.data).first()
                                meet = Meetings(university=session.get('university'),
                                                study_course=session.get('study_course'),
                                                subject_id=sub.subject_id, email_tutor="",
                                                email_headgroup=session.get('email'),
                                                max_members=cform.max_members.data, num_participants=1,
                                                date=cform.date.data,
                                                hour=cform.hour.data)

                                db.session.add(meet)
                                db.session.commit()

                                user = Student.query.filter_by(email=session.get('email')).first()
                                meet.students.append(user)
                                db.session.commit()
                                send_email(cform.email_tutor.data, meet.id, **kwargs)

                                return redirect(url_for('meets.mygroups'))
                    flash('You have inserted a tutor of subjects you do not attend')
                    return redirect(url_for('meets.create'))
            else:
                flash('The student inserted is not a tutor')
                return redirect(url_for('meets.create'))
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
            return redirect(url_for('meets.mygroups'))

    return render_template('create.html', cform=cform)

@meets.route('/add/<int:id>/', methods=["GET", "POST"])
def add(id, **kwargs):
    group = Meetings.query.filter_by(id=id).first()
    aform = FormAdd()

    if aform.validate_on_submit():
        if group.email_tutor != "":
            flash('The group already has a tutor')
            return redirect(url_for('meets.add', id=id))
        tutor = Tutor.query.filter_by(email=aform.email.data).first()
        if tutor:
            for i in tutor.subjects:
                if i.subject_id == group.subject_id:
                    send_email(aform.email.data, group.id, **kwargs)
                    return redirect(url_for('meets.mygroups'))

            flash('The email inserted is referred to a person that is not a tutor of the subject of the group')
            return redirect(url_for('meets.add', id=id))
        else:
            flash('The email inserted is referred to a person that is not a tutor')
            return redirect(url_for('meets.add', id=id))
    return render_template('add_tutor.html', aform=aform, group=group)

@meets.route('/tutors/', methods=["GET", "POST"])
def tutors():
    tform = FormTutors()
    list_subjects = []
    for i in Subjects.query.filter_by(university=session.get('university'), study_course=session.get('study_course')):
        list_subjects.append(i)

    tform.subject.choices = list_subjects
    list_tutors = []
    if tform.validate_on_submit():
        subject = Subjects.query.filter_by(subject=tform.subject.data, university=session.get('university'),
                                           study_course=session.get('study_course')).first()
        tutors = Tutor.query.filter_by(university=session.get('university'))
        list_tutors = []
        for i in tutors:
            for k in i.subjects:
                if k.subject_id == subject.subject_id:
                    if i.average_rating != None:
                        list_tutors.append(i)
        list_tutors.sort(key=lambda x: x.average_rating, reverse=True)

        for i in tutors:
            for k in i.subjects:
                if k.subject_id == subject.subject_id:
                    if i.average_rating == None:
                        list_tutors.append(i)

        if not list_tutors:
            flash("Sorry the subject has no tutors")
            return redirect(url_for('meets.tutors'))

    return render_template('tutors.html', tform=tform, list_tutors=list_tutors)