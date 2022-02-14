from tkinter import Message

from flask import render_template

from project import mail

def send_email(email, id, **kwargs):
    s = str(id)
    msg = Message('Unibuddy Account -- Request of tutor', recipients=[email], sender='unibuddywebsite@gmail.com')
    msg.body = render_template('email.txt', s=s, **kwargs)
    mail.send(msg)
