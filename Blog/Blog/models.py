from Blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#Table Users 
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    education = db.Column(db.String(120), nullable=False)
    job = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    checked = db.Column(db.Boolean, nullable=False, default = False)
    date_created = db.Column(db.DateTime, unique=True, nullable=False,default= datetime.utcnow)
    role = db.Column(db.String(120), nullable=False,default="normal")
    #posts = db.relationship('Post', backref='author', lazy=True) #NOT A COLUMN

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#Table Posts
class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}')"


class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Posts_Comments(db.Model):
    __tablename__ = 'posts_comments'
    post_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('comment_id', 'post_id'),
    )