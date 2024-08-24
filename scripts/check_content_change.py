import hashlib
import requests
import json
import os
import sys

urls = sys.argv[1].splitlines()

state_file = 'previous_states.json'

if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        previous_states = json.load(f)
else:
    previous_states = {}

current_states = {}
changed_urls = []

for url_data in urls:
    parts = url_data.split(';')
    url = parts[0]
    headers = {header.split(':')[0]: header.split(':')[1] for header in parts[1:]}
    
    response = requests.get(url, headers=headers)
    content_hash = hashlib.sha256(response.content).hexdigest()
    current_states[url] = content_hash
    
    if url in previous_states and previous_states[url] != content_hash:
        changed_urls.append(url)

with open(state_file, 'w') as f:
    json.dump(current_states, f)

print('; '.join(changed_urls))
