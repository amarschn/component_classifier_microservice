from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class StepUploadForm(FlaskForm):
    step_file = FileField('STEP File', validators=[FileRequired()])
    submit = SubmitField('Upload')

# def StepUploadForm():
# 	print("hiya")