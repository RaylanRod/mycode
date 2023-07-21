#!/usr/bin/env python3
import requests
from pprint import pprint

URL = "http://127.0.0.1:2224/weather"  # Use the '/weather' endpoint for the POST request
city = "Seattle"  # Replace this with the city you want to get the weather for

# Make a POST request with the 'city' data in the payload
resp = requests.post(URL, data={'city': city}).json()

pprint(resp)
