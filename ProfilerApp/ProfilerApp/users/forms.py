from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ProfilerApp import bcrypt
from ProfilerApp.models import Users
from flask_login import current_user

class LoginForm(FlaskForm):
  email = StringField('Email', 
                              validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')


class changePasswordForm(FlaskForm):
  password = PasswordField('Current Password')
  new_password = PasswordField('New Password',validators=[DataRequired(),Length(min=6,max=21)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('new_password')])
  submit = SubmitField('Update')

  def validate_password(self,password):
      user = Users.query.filter_by(user_id = current_user.get_id()).first()
      if(not bcrypt.check_password_hash(user.password, password.data)):
          raise ValidationError("Wrong Password.")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')