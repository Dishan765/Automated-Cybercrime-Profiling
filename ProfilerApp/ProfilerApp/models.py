from ProfilerApp import db
from datetime import datetime
from flask_login import UserMixin
from ProfilerApp import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#Table Users 
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, unique=True, nullable=False,default= datetime.utcnow)
    role = db.Column(db.String(120), nullable=False,default="normal")

    def get_id(self):
        return self.user_id


#Table Posts
class Profiles(db.Model):
    __tablename__ = 'profiles'
    profile_id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String(120), nullable=False)
    job = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}')"


class SuspiciousComments(db.Model):
    __tablename__ = 'suspicious_comments'
    comment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    profile_id = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)

class SuspiciousPosts(db.Model):
    __tablename__ = 'suspicious_posts'
    post_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    profile_id = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)