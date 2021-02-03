import os
from flask import current_app
from PIL import Image
from flaskapp import db
from flaskapp.models import Job, User

def DefaultImgToThumb(dimensions_tuple):
    thumb_img_size = dimensions_tuple
    img_path = os.path.join(current_app.root_path, 'static/profile_pics/default.jpg')
    img = Image.open(img_path)
    if img.size == thumb_img_size:
        return
    else:
        img.thumbnail(thumb_img_size)
        img.save(img_path)
