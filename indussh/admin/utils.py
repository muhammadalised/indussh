import os
import re
import secrets
from PIL import Image
from flask import url_for, current_app


def save_picture(form_picture, folder_path, size):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, folder_path, picture_fn)

    output_size = size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def clean_text(raw_text):
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_text)
    
    return clean_text