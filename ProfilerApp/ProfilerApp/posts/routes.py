from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login.utils import login_required
from ProfilerApp.users.forms import LoginForm
from ProfilerApp.models import SuspiciousComments, SuspiciousPosts, Users
from ProfilerApp import db, bcrypt
from flask_login import login_user, current_user

posts = Blueprint("posts", __name__)

@posts.route('/posts/suspiciousPost')
@login_required
def suspiciousPosts():
    page = request.args.get('page', 1, type=int)
    posts = SuspiciousPosts.query.order_by(SuspiciousPosts.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('post.html', posts=posts)


@posts.route('/posts/suspiciousComment')
@login_required
def suspiciousComments():
    page = request.args.get('page', 1, type=int)
    comments = SuspiciousComments.query.order_by(SuspiciousComments.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('comment.html', comments=comments)