from flask import Blueprint
from flask import render_template, request, Blueprint
from Blog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
  posts = Post.query.all()
  return render_template('home.html', posts=posts)