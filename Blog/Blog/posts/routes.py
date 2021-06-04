from Blog.api.routes import new_comment, new_comment_hook,new_post_hook
from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from Blog import db
from Blog.models import Posts,Users,Comments
from Blog.posts.forms import PostForm,commentForm
from sqlalchemy import and_


posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods = ['GET' , 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    author_id=current_user.get_id()
    post = Posts(title=title, content=form.content,author_id=author_id)
    db.session.add(post)
    db.session.commit()
    new_post_hook(post.post_id,title,content,author_id,post.date_posted.strftime("%Y-%m-%d %H:%M:%S"))
    flash('Your post has been created', 'success')
    return redirect(url_for('main.home'))
  
  return render_template('create_post.html', form=form)


@posts.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    #Post with post_id
    post =db.session.query(Posts,Users).join(Users).filter(Posts.post_id == post_id).first()

    #No of comments for this post
    comment_count = db.session.query(Comments).filter(Comments.post_id == post_id).count()

    #All comments for this post
    #comments = db.session.query(Comments).filter(Comments.post_id == post_id).all()
    comments = db.session.query(Comments,Users).filter(and_(Comments.post_id == post_id, Comments.author_id == Users.user_id)).order_by(Comments.date_posted.desc()).all()
    #print(comments.Comments.)

    #Logged user's name
    logged_user = Users.query.filter(Users.user_id == current_user.get_id()).first()

    #Form to post comment
    form = commentForm()
    if(form.validate_on_submit()):#POST + FORM FIELDS VALIDATED
        content = form.content.data
        author_id = current_user.get_id()
        comment = Comments(content =content,author_id = author_id,post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        new_comment_hook(comment.comment_id,content,author_id,comment.date_posted.strftime("%Y-%m-%d %H:%M:%S"))
        flash("Your comment has been posted.")
        return redirect(url_for('posts.post', post_id=post_id))  
    else:
        return render_template('post.html', post=post,comment_count =comment_count,comments = comments,form=form,logged_user=logged_user)
    
    


# @posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Posts.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('posts.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html',form=form)


# @posts.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Posts.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('main.home'))