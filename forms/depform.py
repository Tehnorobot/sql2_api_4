from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название отдела', validators=[DataRequired()])
    chief = StringField('Фамилия и Имя руководителя', validators=[DataRequired()])
    members = StringField('id участников', validators=[DataRequired()])
    department_email = StringField('email отдела', validators=[DataRequired()])
    submit = SubmitField('Применить')