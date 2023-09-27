from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired

from config import db

from models import User, Survey


class Surveyform(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    variant_1 = StringField('1 Variant', validators=[DataRequired()])
    variant_2 = StringField('2 Variant', validators=[DataRequired()])
    submit = SubmitField('Add survey')


class SurveyUpdateform(FlaskForm):
    question = StringField('Question', default='')
    variant_1 = StringField('1 Variant', default='')
    variant_2 = StringField('2 Variant', default='')
    submit = SubmitField('Add survey', default='')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired()])

    def validate_on_submit(self, extra_validators=None):
        isUser = User.query.filter_by(email=self.email.data).first()
        print(self.password1, self.password2, sep='|||')
        return self.is_submitted() and self.validate(
            extra_validators=extra_validators) and self.password1.data == self.password2.data and not isUser


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
