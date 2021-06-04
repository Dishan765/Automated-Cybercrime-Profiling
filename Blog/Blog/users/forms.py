from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.fields.core import RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Required
from wtforms_components import DateRange
from flask_login import current_user
from Blog.models import Users
from datetime import date
import datetime


class RegistrationForm(FlaskForm):
  first_name = StringField('First Name', 
                            validators=[DataRequired(),Length(min=2,max =20)])
  last_name = StringField('Last Name', 
                            validators=[DataRequired(),Length(min=2,max =20)])
  email = StringField('Email', 
                              validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  DOB = DateField('Date of Birth', validators=[Required()],format='%Y-%m-%d',)
  education = SelectField('Education', choices=['Primary','Secondary','Tertiary'])
  job = SelectField('Job Status',choices=['Unemployed','Employed','Student'])
  gender = RadioField('Gender', choices=['Male','Female','Others'],validators=[DataRequired(),])

  submit = SubmitField('Sign Up')

  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('This email is already taken.User another one.')

  def validate_DOB(self, DOB):
      todays_date = date.today()
      if(DOB.data >todays_date):
          raise ValidationError('Date of Birth cannnot be in the future')

      time_diff = todays_date -  DOB.data
      age = time_diff.days/365
      if age < 16:
          raise ValidationError('You should be above 16 years old to register.')


class LoginForm(FlaskForm):
  email = StringField('Email', 
                              validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
  username = StringField('Username', 
                            validators=[DataRequired(),Length(min=2,max =20)])
  
  email = StringField('Email', 
                              validators=[DataRequired(), Email()])

  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

  submit = SubmitField('Update')

  def validate_username(self, username):
    if username.data !=current_user.username:
      user = Users.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('This username is already taken.User another one.')
  
  def validate_email(self, email):
    if email.data !=current_user.email:
      user = Users.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('This email is already taken.User another one.')
