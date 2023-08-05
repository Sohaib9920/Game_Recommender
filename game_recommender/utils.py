from game_recommender import app, mail
import secrets
import os
from PIL import Image
from flask import url_for
from flask_mail import Message


def save_picture(form_picture):
    # form_picture is the picture object from form.picture.data
    # In order to save this image, we need to provide full path to where we want to save as well as filename
    # The picture filename should be a random hex with same file extension so that different pictures dont have same name

    random_hex = secrets.token_hex(8) # Getting random hex name
    _ , f_ext = os.path.splitext(form_picture.filename) # Getting file extension
    picture_filename = random_hex + f_ext # Making picture filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename) # Generating full path to where it should be saved
    
    # Changing the size of image in order to save space on file system and speedup website
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Saving the picture
    i.save(picture_path) 
    return picture_filename

def send_reset_message(user):
    # Create a token for this user which will be valid for default 30 min
    token = user.get_reset_token()
    subject = "Password Reset Request"
    sender = "sohaib9920.ahmed@gmail.com"
    recipients = [user.email]
    body = f"""To reset your password, visit the following link:
{url_for("reset_token", token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    # _external to get fixed url. No indent in doc string because thay will be included in email
    message = Message(subject=subject, sender=sender, recipients=recipients, body=body)
    # Send the message
    mail.send(message)