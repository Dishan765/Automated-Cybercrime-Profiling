from flask import Blueprint
from flask import render_template, request, Blueprint
from Blog.models import Posts,Comments, Users
from Blog import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    comment_count = [] #No of comments for each post_id returned in posts
    posts=db.session.query(Posts,Users).join(Users).order_by(Posts.date_posted.desc()).all()

    #Get no of comments for each post_id in posts
    for post in posts:
        post_id = post.Posts.post_id
        comment_count_per_post = db.session.query(Comments).filter(Comments.post_id == post_id).count()
        comment_count.append(comment_count_per_post)

        #comment_count = 3

    #print(comment_count)
    return render_template('home.html', posts=posts,comment_count = comment_count)





