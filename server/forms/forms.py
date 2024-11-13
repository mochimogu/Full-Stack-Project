from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    content = StringField("Enter Content", validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    updateContent = StringField("Update Content", validators=[DataRequired()])
    submit = SubmitField('Update')