from Blog.api.routes import new_comment, new_comment_hook, new_post_hook
from flask import Blueprint,session
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from Blog import db
from Blog.models import Posts, Users, Comments
from Blog.posts.forms import PostForm, commentForm, editCommentForm,editPostForm
from sqlalchemy import and_
import datetime
from Blog.posts.utils import suspicious_comment_detect,suspicious_post_detect


posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    if not current_user.is_authenticated:
        flash("Login to create a post", 'warning')
        return redirect(url_for('main.home'))

    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        flash("Confirm your acccount to create a post", 'warning')
        return redirect(url_for('main.home'))

    
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author_id = current_user.get_id()
        post = Posts(title=title, content=content, author_id=author_id)
        db.session.add(post)
        db.session.commit()
        new_post_hook(post.post_id,title,content,author_id,post.date_posted.strftime("%Y-%m-%d %H:%M:%S"))

        session['last_url'] = url_for("posts.new_post")
        if suspicious_post_detect(title,content):
            flash('Your post violates the ICT act.','warning')
        else:
            flash('Your post has been created.','success')
        return redirect(url_for("posts.your_posts"))

    session['last_url'] = url_for("posts.new_post")    
    return render_template("create_post.html", form=form,checked = checked)


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    # Post with post_id
    post = (
        db.session.query(Posts, Users)
        .join(Users)
        .filter(Posts.post_id == post_id)
        .first()
    )

    # No of comments for this post
    comment_count = (
        db.session.query(Comments).filter(Comments.post_id == post_id).count()
    )

    # All comments for this post
    # comments = db.session.query(Comments).filter(Comments.post_id == post_id).all()
    comments = (
        db.session.query(Comments, Users)
        .filter(and_(Comments.post_id == post_id, Comments.author_id == Users.user_id))
        .order_by(Comments.date_posted.desc())
        .all()
    )
    # print(comments.Comments.)

    # Logged user's name
    logged_user = Users.query.filter(Users.user_id == current_user.get_id()).first()

    # Form to post comment
    form = commentForm()
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked

    if form.validate_on_submit():  # POST + FORM FIELDS VALIDATED
        content = form.content.data
        author_id = current_user.get_id()
        comment = Comments(content=content, author_id=author_id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        new_comment_hook(comment.comment_id,content,author_id,comment.date_posted.strftime("%Y-%m-%d %H:%M:%S"))
        
        if suspicious_comment_detect(content):
            flash('Your comment violates the ICT act.','warning')
        else:
            flash("Your comment has been posted.",'success')

        # redirect user to specific post after deleting comment by storing
        # session variable
        session['last_url'] = url_for("posts.post", post_id=post_id)

        return redirect(url_for("posts.post", post_id=post_id))
    else:
        session['last_url'] = url_for("posts.post", post_id=post_id)
        return render_template(
            "post.html",
            post=post,
            comment_count=comment_count,
            comments=comments,
            form=form,
            logged_user=logged_user,
            checked = checked
        )


@posts.route("/post/your_posts")
@login_required
def your_posts():
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        flash("Confirm your acccount to see your posts", 'warning')
        return redirect(url_for('main.home'))

    page = request.args.get('page', 1, type=int)
    comment_count = []  # No of comments for each post_id returned in posts
    posts = Posts.query.filter_by(author_id=current_user.get_id()).order_by(Posts.date_posted.desc()).paginate(page=page,per_page=5)
    # Get no of comments for each post_id in posts
    for post in posts.items:
        post_id = post.post_id
        comment_count_per_post = (
            db.session.query(Comments).filter(Comments.post_id == post_id).count()
        )
        comment_count.append(comment_count_per_post)
    
    session['last_url'] = url_for("posts.your_posts")    
    return render_template("your_posts.html", posts=posts, comment_count=comment_count,checked=checked)

@posts.route("/post/your_comments", methods=['POST','GET'])
@login_required
def your_comments():
    if not current_user.is_authenticated:
        flash("Login to create a post", 'warning')
        return redirect(url_for('main.home'))

    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        flash("Confirm your acccount to see your comments", 'warning')
        return redirect(url_for('main.home'))

    page = request.args.get('page', 1, type=int)
    comments = Comments.query.filter_by(author_id=current_user.get_id()).paginate(page=page,per_page=5)
    session['last_url'] = url_for("posts.your_comments")
    return render_template("your_comments.html",comments=comments,checked=checked)

@posts.route(
    "/post/update_comment/<int:post_id>/<int:comment_id>", methods=["GET", "POST"]
)
@login_required
def update_comment(post_id, comment_id):

    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        return redirect(url_for('main.home'))

    form = editCommentForm()
    # Post with post_id
    post = (
        db.session.query(Posts, Users)
        .join(Users)
        .filter(Posts.post_id == post_id)
        .first()
    )

    # No of comments for this post
    comment_count = (
        db.session.query(Comments).filter(Comments.post_id == post_id).count()
    )

    # All comments for this post
    # comments = db.session.query(Comments).filter(Comments.post_id == post_id).all()
    comments = (
        db.session.query(Comments, Users)
        .filter(and_(Comments.post_id == post_id, Comments.author_id == Users.user_id))
        .order_by(Comments.date_posted.desc())
        .all()
    )

    if form.validate_on_submit():  # POST + FORM FIELDS VALIDATED
        content = form.content.data
        comment = Comments.query.filter_by(comment_id=comment_id).first()
        comment.content = content
        comment.date_posted = datetime.datetime.utcnow()
        db.session.commit()
        new_comment_hook(comment.comment_id,comment.content,comment.author_id,comment.date_posted.strftime("%Y-%m-%d %H:%M:%S"))
        
        if suspicious_comment_detect(content):
            flash('Your comment violates the ICT act.','warning')
        else:
            flash("Your comment has been edited.","success")
        
        if session.get('last_url') is None:
            return redirect(url_for("posts.post", post_id=post_id))
        else:
            specific_post_url = session['last_url']
            session.pop('last_url', None)
            print(specific_post_url)
            return redirect(specific_post_url)
    else:
        return render_template(
            "EditComment.html",
            post=post,
            comment_count=comment_count,
            comments=comments,
            form=form,
            comment_id=comment_id
        )


@posts.route("/post/<int:comment_id>/delete_comment", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        return redirect(url_for('main.home'))

    comment = Comments.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')

    if session.get('last_url') is None:
        return redirect(url_for('post.yourPosts'))
    else:
        specific_post_url = session['last_url']
        session.pop('last_url', None)
        print(specific_post_url)
        return redirect(specific_post_url)
        


@posts.route("/post/<int:post_id>/update_post", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked
    if current_user.is_authenticated and not checked:
        return redirect(url_for('main.home'))

    post = Posts.query.get_or_404(post_id)
    form = editPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.datetime.utcnow()
        db.session.commit()
        new_post_hook(post.post_id,post.title,post.content,post.author_id,post.date_posted.strftime("%Y-%m-%d %H:%M:%S"))

        if suspicious_post_detect(post.title,post.content):
            flash('Your post violates the ICT act.','warning')
        else:
            flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("EditPost.html", form=form,post_id=post_id)


@posts.route("/post/<int:post_id>/delete_post", methods=['POST','GET'])
@login_required
def delete_post(post_id):
    user = Users.query.filter_by(user_id=current_user.get_id()).first()
    checked = user.checked

    if current_user.is_authenticated and not checked:
        return redirect(url_for('main.home'))

    comments = Comments.query.filter_by(post_id=post_id).all()
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()

    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.your_posts'))


