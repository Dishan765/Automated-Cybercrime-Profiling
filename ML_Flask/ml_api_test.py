import requests
import json

url="http://localhost:9000/ml_api"
data=json.dumps({'sentence':'To ene falco toi'})
r=requests.post(url,data)
print(r.json())

