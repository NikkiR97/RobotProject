import requests
url = 'http://localhost/RobotApi/api/map/create.php'
data = ''' {
    "x" : 15,
    "y" : 15,
    "detected" : 0,
    "traveled" : 0,
    "obstacle" : 1
} '''
response = requests.post(url, data=data)

print(response)