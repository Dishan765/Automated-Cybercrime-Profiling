from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login.utils import login_required
from ProfilerApp.users.forms import LoginForm
from ProfilerApp.models import SuspiciousComments, Users,SuspiciousPosts,Profiles
from ProfilerApp import db, bcrypt
from flask_login import login_user, current_user,logout_user
from sqlalchemy import func

profile = Blueprint("profile", __name__)

@profile.route('/<string:profile_type>')
@profile.route('/home/<string:profile_type>')
@profile.route('/profile/summaryProfile/<string:profile_type>')
@login_required
def summaryProfile(profile_type):
    if profile_type == "age":
        ageList =[]
        age_countList = []
        agesDB = db.session.query(Profiles.age, func.count(Profiles.age)).group_by(Profiles.age).all()
        for age,age_count in agesDB:
            ageList.append(age)
            age_countList.append(age_count)
        return render_template('summary_profile.html',x_values=ageList,y_values=age_countList,profile_type=profile_type)
    elif profile_type == "education":
        educationList =[]
        education_countList = []
        educationsDB = db.session.query(Profiles.education, func.count(Profiles.education)).group_by(Profiles.education).all()
        for education,education_count in educationsDB:
            educationList.append(education)
            education_countList.append(education_count)
        return render_template('summary_profile.html',x_values=educationList,y_values=education_countList,profile_type=profile_type)
    elif profile_type == "employment":
        jobList =[]
        job_countList = []
        jobsDB = db.session.query(Profiles.job, func.count(Profiles.job)).group_by(Profiles.job).all()
        for job,job_count in jobsDB:
            jobList.append(job)
            job_countList.append(job_count)
        return render_template('summary_profile.html',x_values=jobList,y_values=job_countList,profile_type=profile_type)
    elif profile_type == "gender":
        genderList =[]
        gender_countList = []
        gendersDB = db.session.query(Profiles.gender, func.count(Profiles.gender)).group_by(Profiles.gender).all()
        for gender,gender_count in gendersDB:
            genderList.append(gender)
            gender_countList.append(gender_count)
        return render_template('summary_profile.html',x_values=genderList,y_values=gender_countList,profile_type=profile_type)
#age = db.session.query(Profiles.education, func.count(Profiles.education)).group_by(Profiles.education).all()


#post_id or comment_id
@profile.route('/profile/post_profile/<int:post_id>')
@login_required
def post_profile(post_id):
    post = SuspiciousPosts.query.filter_by(post_id=post_id).first()
    profile = Profiles.query.filter_by(profile_id=post.profile_id).first()
    return render_template('post_profile.html',post=post,profile=profile)

@profile.route('/profile/comment_profile/<int:comment_id>')
@login_required
def comment_profile(comment_id):
    comment = SuspiciousComments.query.filter_by(comment_id=comment_id).first()
    profile = Profiles.query.filter_by(profile_id=comment.profile_id).first()
    return render_template('comment_profile.html',comment=comment,profile=profile)