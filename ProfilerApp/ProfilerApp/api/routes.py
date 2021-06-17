from flask import Blueprint,request,abort
from ProfilerApp.models import Profiles, SuspiciousComments, SuspiciousPosts
from ProfilerApp import db
import json
import requests

api = Blueprint('api', __name__)

@api.route('/api/new_comment', methods = ['POST'])
def new_comment():
    #return render_template('home.html')
    if request.method == 'POST':
        #print(request.json)
        comment_info = request.json
        print(comment_info['content'])
        ml_url="http://localhost:9000/ml_api"
        comment=json.dumps({'sentence':comment_info['content']})
        suspiciousFound =requests.post(ml_url,comment)
        print(suspiciousFound.json())

        author_id = comment_info['author_id']
        if(suspiciousFound.json() == 1):
            author_details_url = "http://localhost:3000/api/user_details"
            author_id_json = json.dumps({'author_id':author_id})
            author_data = requests.post(author_details_url, author_id_json)
            author_details = author_data.json()
            exists_author = db.session.query(db.exists().where(Profiles.profile_id == author_id)).scalar()
            #Insert new profile information in DB if not already inserted
            if not exists_author:
                profiles = Profiles(profile_id = author_id, education = author_details['education'],age=author_details['age'],gender = author_details['gender'],job = author_details['job'])
                db.session.add(profiles)
                db.session.commit()

            #Insert comment information in DB
            comment = SuspiciousComments(content = comment_info['content'],profile_id = author_id,date_posted = comment_info['date_posted'])
            db.session.add(comment)
            db.session.commit()
            
        
        return 'success',200
    else:
        return abort(400)


@api.route('/api/new_post', methods = ['POST'])
def new_post():
    if request.method == 'POST':
        # Web hook post information in JSON format
        post_info = request.json

        # Suspicious Text Detector API URL
        ml_url="http://localhost:9000/ml_api"

        # Title of post
        comment=json.dumps({'sentence':post_info['title']})
        # Calling Suspicious Text Detector API to classify title
        suspiciousFound =requests.post(ml_url,comment)
        # Predicted label for post
        suspiciousTitle  = suspiciousFound.json()

        # Conent of post
        comment=json.dumps({'sentence':post_info['content']})
        # Calling Suspicious Text Detector API to classify content
        suspiciousFound =requests.post(ml_url,comment)
        # Predicted label for content
        suspiciousContent  = suspiciousFound.json()

        # author_id of post 
        author_id = post_info['author_id']
        # if either tile or contnet ==1 i.e. suspicious 
        if(suspiciousTitle == 1 or suspiciousContent==1):
            # offender informaiton API URL
            author_details_url = "http://localhost:3000/api/user_details"
            author_id_json = json.dumps({'author_id':author_id})
            # Call offender informaiton API 
            author_data = requests.post(author_details_url, author_id_json)
            author_details = author_data.json()

            exists_author = db.session.query(db.exists().where(Profiles.profile_id == author_id)).scalar()
            
            #Insert new profile information in DB if not already inserted
            if not exists_author:
                profiles = Profiles(profile_id = author_id, education = author_details['education'],
                                    age=author_details['age'],gender = author_details['gender'],
                                    job = author_details['job'])
                db.session.add(profiles)
                db.session.commit()

            #Insert comment information in DB
            post = SuspiciousPosts(title=post_info['title'], content = post_info['content'],
                                    profile_id = author_id,date_posted = post_info['date_posted'])
            db.session.add(post)
            db.session.commit()
        return 'success',200
    else:
        return abort(400)

@api.route('/api/update_account', methods = ['POST'])
def update_account():
    if request.method == 'POST':
        # Updated author information from web hook
        account_info = request.json

        # Update profile information in database
        profile = Profiles.query.filter_by(profile_id = account_info['author_id']).first()
        if profile:
            profile.age = account_info['age']
            profile.job = account_info['employment']
            profile.education = account_info['education']
            profile.gender = account_info['gender']
            db.session.commit()
        
        return 'success',200
    else:
        return  abort(400)


    