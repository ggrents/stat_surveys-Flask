from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class Surveyform(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    variant_1 = StringField('1 Variant', validators=[DataRequired()])
    variant_2 = StringField('2 Variant', validators=[DataRequired()])
    submit = SubmitField('Add survey')


class SurveyUpdateform(FlaskForm):
    question = StringField('Question')
    variant_1 = StringField('1 Variant')
    variant_2 = StringField('2 Variant')
    submit = SubmitField('Add survey')


class RegisterForm(FlaskForm) :
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')
