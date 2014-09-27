import requests
import json

LOCATION = 'location1'
BASE_URL = 'https://incandescent-fire-7887.firebaseio.com/'
DATA_URL = BASE_URL + LOCATION + '.json'

r = requests.get(DATA_URL)

print r.json()

data = r.json()

data['trash'] = 20

print type(data)

r = requests.put(DATA_URL, data=json.dumps(data))

print r.text