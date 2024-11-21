import requests
import json

# url = "http://localhost:5000/threat"
url = "http://localhost:9000/classify"

headers = {
    'Content-Type': 'application/json'
}

# data = {
#     "query": "hi anish how are you doing good how are you im fine"
# }

data = {
    "content": "These discrepancies not only disrupt my ability to track and manage my finances accurately but also raise concerns about the reliability and integrity of the online banking system."
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
except:
    print("timeout")