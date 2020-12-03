from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

class ImageUpload(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Enter Room')