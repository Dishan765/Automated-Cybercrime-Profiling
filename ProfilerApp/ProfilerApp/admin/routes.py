from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login.utils import login_required
from ProfilerApp.users.forms import LoginForm,changePasswordForm
from ProfilerApp.admin.forms import AddAccountForm
from ProfilerApp.models import Users
from ProfilerApp import db, bcrypt
from flask_login import login_user, current_user,logout_user
from ProfilerApp.admin.utils import generate_password,send_email

admin = Blueprint("admin", __name__)

@admin.route("/admin", methods=["GET", "POST"])
def adminLogin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin.listAccount'))

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role=='admin':
            login_user(user, form.remember.data)
            flash(f"Login Successfully.", "success")
            return redirect(url_for("admin.listAccount"))
        else:
            flash(f"Wrong username or password.", "danger")
    return render_template("login.html", form=form)

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@admin.route("/admin/account",methods=["GET", "POST"])
@login_required
def account():
    form = changePasswordForm()
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Account details updated successfully.",'success')
        redirect(url_for('admin.account'))
    return render_template('adminAccount.html',form=form,email=user.email)

@admin.route("/admin/listAccount",methods=["GET", "POST"])
@login_required
def listAccount():
    users = Users.query.filter(Users.role != 'admin').all()
    return render_template('adminListAcc.html',users=users)


@admin.route("/admin/createAccount",methods=["GET", "POST"])
@login_required
def createAccount():
    form = AddAccountForm()
    if form.validate_on_submit():
        pwd = generate_password()
        hashed_password = bcrypt.generate_password_hash(pwd).decode("utf-8")
        user = Users(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        html = render_template('pwdEmail.html', password=pwd)
        subject = "Account Created for ProfilerApp"
        send_email(user.email, subject, html)
        flash("Account details updated successfully. The password has been sent to the user.",'success')
        return redirect(url_for('admin.listAccount'))
    
    return render_template('adminAddAcc.html',form=form)


@admin.route("/admin/deleteAccount/<int:user_id>",methods=["GET", "POST"])
@login_required
def deleteAccount(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash(f'User with email {user.email} deleted sucessfully.','success')
    return redirect(url_for('admin.listAccount'))



