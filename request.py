import requests
import json

# url = "http://localhost:5000/threat"
url = "http://localhost:5000/classify"

headers = {
    'Content-Type': 'application/json'
}

# data = {
#     "query": "hi anish how are you doing good how are you im fine"
# }

data = {
    "content": "this is very urgent that the march 2002 settlement agreement following is an analysis of the change in net revenue comparing 2003 to 2002. ."
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
except:
    print("timeout")