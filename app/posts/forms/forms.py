"""
The module for Posts Form.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0
"""


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """ PostForm for user to posts"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
