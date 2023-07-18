#!/usr/bin/env python3
"""Returning the location of the ISS in latitude/longitude"""
import requests

URL= "http://api.open-notify.org/iss-now.json"
def main():
    resp= requests.get(URL).json()
    
    lat = resp['iss_position']['latitude']
    lon = resp['iss_position']['longitude']

    print(f'CURRENT LOCATION OF THE ISS: \n' 
          f'  lon: {lon}\n'
          f'  lat: {lat}\n'
    )

if __name__ == "__main__":
    main()

