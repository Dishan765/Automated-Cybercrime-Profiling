from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from Blog import db, bcrypt
from Blog.models import Users, Posts
from Blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm,ResetPasswordForm
from Blog.users.utils import save_picture
from Blog.utils import age, save_picture
from Blog.users.token import confirm_token,generate_confirmation_token
from Blog.users.email import send_email
import datetime
from Blog.api.routes import update_account_hook
from datetime import timedelta
from flask import current_app

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():  # POST + FORM FIELDS VALIDATED
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        dob = form.DOB.data
        age_calc = age(dob)
        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            dob=dob,
            age=age_calc,
            password=hashed_password,
            education=form.education.data,
            job=form.job.data,
            gender=form.gender.data,
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('activate_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        flash(f'Registration Successful. Login Now.', 'success')
        return redirect(url_for("users.login"))
    else:
        return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)

            session.permanent = True
            current_app.permanent_session_lifetime = timedelta(minutes=60)

            flash(f"Login Successfully.", "success")
            return redirect(url_for("main.home"))
        else:
            flash(f"Wrong username or password.", "danger")
    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    user = Users.query.filter_by(user_id=current_user.get_id()).first()

    if form.validate_on_submit():
        if form.email.data != user.email:
            user.checked = False
            user.email = form.email.data
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('users.confirm_email', token=token, _external=True)
            html = render_template('activate_email.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender = form.gender.data
        user.dob = form.DOB.data
        user.age = age(user.dob)
        user.education = form.education.data
        user.job = form.job.data
        db.session.commit()
        update_account_hook(user.user_id,user.age,user.job,user.education,user.gender)
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.gender.data = user.gender
        form.DOB.data = user.dob
        form.education.data = user.education
        form.job.data = user.job
        form.email.data = user.email
        
    image_file = url_for("static", filename="Images/" + user.image_file)

    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    return render_template("account.html", form=form, image_file=image_file,checked =checked)


@users.route('/users/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(email=email).first_or_404()
    if user.checked:
        flash('Account already checked.', 'success')
    else:
        user.checked = True
        db.session.add(user)
        db.session.commit()
        flash('You have checked your account. Thanks!', 'success')
    return redirect(url_for("main.home"))

@users.route('/users/resend')
@login_required
def resend_confirmation():
    user = Users.query.filter_by(email=current_user.email).first_or_404()
    if user.checked:
        flash('Account already checked.', 'success')
        if session.get('last_url') is None:
            return redirect(url_for('post.yourPosts'))
        else:
            specific_post_url = session['last_url']
            session.pop('last_url', None)
            print(specific_post_url)
            return redirect(specific_post_url)

    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('activate_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    if session.get('last_url') is None:
        return redirect(url_for('main.home'))
    else:
        specific_post_url = session['last_url']
        session.pop('last_url', None)
        print(specific_post_url)
        return redirect(specific_post_url)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect( url_for('main.home'))
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
        return redirect( url_for('main.home'))
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
