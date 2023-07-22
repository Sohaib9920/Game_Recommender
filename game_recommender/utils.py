from game_recommender import app
import secrets
import os
from PIL import Image


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

