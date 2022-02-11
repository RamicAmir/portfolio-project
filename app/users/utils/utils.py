"""
The module for User Utils.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0.1
"""

import os
import secrets
from PIL import Image
from app import mail
from flask_mail import Message
from flask import url_for, current_app


def save_picture(form_picture):
    # To save user's picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Handler image size
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn


def send_reset_email(user):
    # To send reset_email for user request
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
