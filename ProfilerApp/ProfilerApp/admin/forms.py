from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ProfilerApp import bcrypt
from ProfilerApp.models import Users
from flask_login import current_user


class AddAccountForm(FlaskForm):
    first_name = StringField('First Name', 
                                validators=[DataRequired(),Length(min=2,max =20)])
    last_name = StringField('Last Name', 
                                validators=[DataRequired(),Length(min=2,max =20)])
    email = StringField('Email', 
                                validators=[DataRequired(), Email()])

    
    submit = SubmitField('Add Account')


