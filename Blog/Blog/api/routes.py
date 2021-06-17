from flask import Blueprint,request,jsonify,abort,session,redirect,url_for,flash
from Blog.models import Users
import requests
import json

api = Blueprint('api', __name__)

#web hook that calls profiler api when a new comment is posted
#@api.route('/new_comment', methods=['POST'])
def new_comment(comment_id,content,author_id,date_posted):
    profiler_url = "http://127.0.0.1:4000/api/new_comment"# url to send data (profiler API)
    data = {"comment_id": comment_id,
            "content": content,
            "author_id":author_id,
            "date_posted":date_posted}
    requests.post(profiler_url,data =json.dumps(data),headers ={'Content-Type':'application/json'}  )
    
def new_comment_hook(comment_id,content,author_id,date_posted):
    profiler_url = "http://127.0.0.1:4000/api/new_comment"# url to send data (profiler API)
    data = {"comment_id": comment_id,
            "content": content,
            "author_id":author_id,
            "date_posted":date_posted}
    requests.post(profiler_url,data =json.dumps(data),headers ={'Content-Type':'application/json'}  )

#api that returns user details from author_id 
@api.route('/api/user_details',methods=['POST'])
def user_details():
    if request.method == 'POST':
        author_data = request.get_json(force=True)
        # Author id to be profiled
        author_id = author_data['author_id']
        # Get author information from database
        author_details_dict = {}
        author_details = Users.query.filter_by(user_id=author_id).first()
        author_details_dict["education"] = author_details.education
        author_details_dict["age"] = author_details.age
        author_details_dict["job"] = author_details.job
        author_details_dict["gender"] = author_details.gender

        #return author informaition in JSON format
        return jsonify(author_details_dict)
    
    jsonify("False")

#web hook that calls profiler api when a new post is posted
def new_post_hook(post_id,title,content,author_id,date_posted):
    profiler_url = "http://127.0.0.1:4000/api/new_post"# url to send data (profiler API)
    data = {"post_id": post_id,
            "title":title,
            "content": content,
            "author_id":author_id,
            "date_posted":date_posted}
    requests.post(profiler_url,data =json.dumps(data),headers ={'Content-Type':'application/json'}  )


#web hook that detects changes in user accounts
def update_account_hook(author_id,age,employment,education,gender):
    # enpoint in Profiling Applicaitn to send updated author information 
    profiler_url = "http://127.0.0.1:4000/api/update_account"

    # New author informaiton 
    data = {"author_id": author_id,
            "age": age,
            "employment":employment,
            "education":education,
            "gender":gender}

    # Sends to updated author informaiton to endpoint in Profling Applicaiton
    requests.post(profiler_url,data =json.dumps(data),headers ={'Content-Type':'application/json'}  )


#consumes a web hook from profiler app when a post/comment is suspicious
@api.route('/api/warn_user',methods=['POST'])
def warn_user():
    if request.method == 'POST':
        suspicious_info = request.json
        if suspicious_info['suspicious'] == 1:
            pass
        return 'success',200
    else:
        abort(400)

