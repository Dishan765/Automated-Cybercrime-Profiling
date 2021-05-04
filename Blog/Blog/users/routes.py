from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Blog import db, bcrypt
from Blog.models import User, Post
from Blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from Blog.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET' , 'POST'])
def register():
  form = RegistrationForm()
  if current_user.is_authenticated:
      return redirect(url_for('main.home'))

  if(form.validate_on_submit()):#POST + FORM FIELDS VALIDATED
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f"Account Created Succesfully for user {form.username.data}. Login Now.", 'success')
    return redirect(url_for('users.login'))  
  else:
    return render_template('register.html', form = form)

@users.route('/login', methods = ['GET' , 'POST'])
def login():
  form = LoginForm()
  if current_user.is_authenticated:
      return redirect(url_for('main.home'))

  if(form.validate_on_submit()):
    user = User.query.filter_by(email = form.email.data).first()
    if (user and bcrypt.check_password_hash(user.password, form.password.data)):
      login_user(user, form.remember.data)
      flash(f"Login Successfully", 'success')
      return redirect(url_for('main.home'))  
    else:
      flash(f"Wrong username or password.", 'danger')
  return render_template('login.html', form = form)


@users.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('main.home'))


@users.route("/account", methods = ['GET' , 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('users.account'))
  elif request.method == "GET":
    form.username.data = current_user.username
    form.email.data = current_user.email
  
  image_file = url_for('static', filename='Images/' + current_user.image_file)
  return render_template('account.html', form=form, image_file=image_file)