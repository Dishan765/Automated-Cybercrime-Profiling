import json, requests


def suspicious_post_detect(title,content):
    ml_url="http://localhost:9000/ml_api"
    title_json=json.dumps({'sentence':title})
    suspiciousFound =requests.post(ml_url,title_json)
    suspiciousTitle  = suspiciousFound.json()

    content_json=json.dumps({'sentence':content})
    suspiciousFound =requests.post(ml_url,content_json)
    suspiciousContent  = suspiciousFound.json()
    
    if(suspiciousTitle == 1 or suspiciousContent==1):
        return 1
    else:
        return 0


def suspicious_comment_detect(comment):
    ml_url="http://localhost:9000/ml_api"
    comment=json.dumps({'sentence':comment})
    suspiciousFound =requests.post(ml_url,comment)
    return suspiciousFound.json()