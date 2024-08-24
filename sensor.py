import hashlib
import requests
import json
import os
import sys
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

CONF_URLS = "urls"
CONF_SCAN_INTERVAL = "scan_interval"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URLS): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=300): cv.positive_int,
    vol.Optional(CONF_NAME, default="Content Change Monitor"): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    urls = config.get(CONF_URLS).splitlines()
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    name = config.get(CONF_NAME)

    add_entities([ContentChangeMonitor(name, urls, scan_interval)], True)

class ContentChangeMonitor(Entity):
    def __init__(self, name, urls, scan_interval):
        self._name = name
        self._urls = urls
        self._scan_interval = scan_interval
        self._state = None
        self._changed_urls = []

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        state_file = 'previous_states.json'
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                previous_states = json.load(f)
        else:
            previous_states = {}

        current_states = {}
        changed_urls = []

        for url_data in self._urls:
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

        self._state = '; '.join(changed_urls)
