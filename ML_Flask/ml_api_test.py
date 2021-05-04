import requests
import json

url="http://localhost:5000/ml_api"
data=json.dumps({'sentence':'pilon.'})
r=requests.post(url,data)
print(r.json())