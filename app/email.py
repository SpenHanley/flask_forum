from flask_mail import Message
from . import app, mail

def send_mail(to, subject, template):
    
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_SENDER']
    )

    mail.send(msg)