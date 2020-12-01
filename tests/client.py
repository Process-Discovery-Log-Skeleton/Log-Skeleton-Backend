import requests
import os

path = os.path.join(
        os.path.dirname(__file__), '../res/logs/paper-example.xes')

f = open(path, "r")
event_log = f.read()
f.close()

print('Loaded log...')

headers = {'Content-Type': 'application/xml'}

print('Calling API...')
response = requests.get('http://localhost:5000/log-skeleton?noise-threshold=-10', data=event_log, headers=headers)

print(response.text)

