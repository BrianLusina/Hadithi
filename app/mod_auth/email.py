from flask import current_app
from app import mail
from flask_mail import Message


def send_mail(to, subject, template):
    """
    Sends a confirmation tmail to the new registering user
    :param to: recipient of this email, the new registering user
    :param subject: The subject of the email
    :param template: The message body
    """
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    mail.send(msg)
