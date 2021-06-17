from flask import Blueprint
from flask import render_template, request, Blueprint
from Blog.models import Posts,Comments, Users
from Blog import db
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    #pagination configuration
    page = request.args.get('page', 1, type=int)
    comment_count = [] #No of comments for each post_id returned in posts
    posts=db.session.query(Posts,Users).join(Users).order_by(Posts.date_posted.desc()).paginate(page=page,per_page=5)

    #Get no of comments for each post_id in posts
    for post in posts.items:
        post_id = post.Posts.post_id
        comment_count_per_post = db.session.query(Comments).filter(Comments.post_id == post_id).count()
        comment_count.append(comment_count_per_post)

        #comment_count = 3

    checked = False
    #print(comment_count)
    if current_user.is_authenticated:
        user = Users.query.filter_by(user_id=current_user.get_id()).first()
        checked = user.checked

    return render_template('home.html', posts=posts,comment_count = comment_count,checked = checked)




    



