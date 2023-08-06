from game_recommender import app, mail
import secrets
import os
from PIL import Image
from flask import url_for
from flask_mail import Message
from game_recommender.models import Rating


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


def add_db_users(current_users_df):
    # Add the users from database into the current users dataframe loaded from csv
    df_last_id = current_users_df.index[-1]
    ratings = Rating.query.all()
    if ratings:
        for rating_object in ratings:
            new_user_id = df_last_id + rating_object.user_id
            game_title = rating_object.game.title
            if new_user_id not in current_users_df.index:
                current_users_df.loc[new_user_id] = 0
            current_users_df.at[new_user_id, game_title] = rating_object.rating