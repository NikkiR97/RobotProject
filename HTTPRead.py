import requests
import json

url = 'http://localhost/RobotApi/api/map/read.php'

response = requests.get(url)

response_json = response.json()

response_parsed = json.dumps(response_json)

print(response_parsed)