import requests
import json

r = requests.get('https://incandescent-fire-7887.firebaseio.com/location1.json')

print r.json()

data = r.json()

data['trash'] = 20

print type(data)

r = requests.put('https://incandescent-fire-7887.firebaseio.com/location1.json', data=json.dumps(data))

print r.text