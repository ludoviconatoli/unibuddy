from flask_mail import Message

from flask import render_template
from project import mail

def send_email(email, id, **kwargs):
    s = str(id)
    msg = Message('Unibuddy Account -- Request of tutor', sender='unibuddywebsite@gmail.com', recipients=[email])
    msg.body = render_template('email.txt', s=s, **kwargs)
    mail.send(msg)
