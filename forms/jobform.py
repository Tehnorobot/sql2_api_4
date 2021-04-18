from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    team_leader = StringField('id командира', validators=[DataRequired()])
    work_size = StringField('Время работы(в часах)', validators=[DataRequired()])
    collaborators = StringField('id команды', validators=[DataRequired()])
    is_private = BooleanField("Работа закончена?")
    submit = SubmitField('Применить')