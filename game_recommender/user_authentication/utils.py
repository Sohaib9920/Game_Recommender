from game_recommender import mail
from flask_mail import Message

def send_reset_message(user, url, app):
    with app.app_context():
        subject = "Password Reset Request"
        sender = "no-reply@GamerInsight.com"
        recipients = [user.email]
        body = f"""To reset your password, visit the following link:
{url}
If you did not make this request then simply ignore this email and no changes will be made.
"""
        message = Message(subject=subject, sender=sender, recipients=recipients, body=body)
        mail.send(message)