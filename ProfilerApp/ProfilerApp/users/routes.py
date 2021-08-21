from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login.utils import login_required
from ProfilerApp.users.forms import LoginForm,changePasswordForm,RequestResetForm,ResetPasswordForm
from ProfilerApp.models import Users
from ProfilerApp import db, bcrypt
from flask_login import login_user, current_user,logout_user
from ProfilerApp.admin.utils import send_email
from ProfilerApp.users.token import confirm_token,generate_confirmation_token
from datetime import timedelta
from flask import current_app

users = Blueprint("users", __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("profile.summaryProfile",profile_type='age'))

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            flash(f"Login Successfully.", "success")
            session.permanent = True
            current_app.permanent_session_lifetime = timedelta(minutes=60)
            return redirect(url_for("profile.summaryProfile",profile_type='age'))
        else:
            flash(f"Wrong username or password.", "danger")
    return render_template("login.html", form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@users.route("/users/account",methods=["GET", "POST"])
def account():
    form = changePasswordForm()
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Account details updated successfully.",'success')
        return redirect(url_for('users.account'))
    return render_template('account.html',form=form,email=user.email)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect( url_for('profile.summaryProfile',profile_type='age'))
    form = RequestResetForm()
    if form.validate_on_submit():
        token = generate_confirmation_token(form.email.data)
        reset_url = url_for('users.reset_password', token=token, _external=True)
        html = render_template('reset_email.html',reset_url = reset_url)
        subject = "Reset Password for ProfilerApp"
        send_email(form.email.data, subject, html)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',form=form)



@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect( url_for('profile.summaryProfile',profile_type='age'))
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=email).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)