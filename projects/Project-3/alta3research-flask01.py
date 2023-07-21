from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Hidden API key
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the request method is POST
    if request.method == 'POST':
        # If it's a POST request, get the 'city' data from the form
        city = request.form['city']
        # Call the get_weather() function with the 'city' data and return the result
        return get_weather(city)
    else:
        # If it's not a POST request (i.e., it's a GET request), render the 'get_city.html' template
        # without trying to access form data, as there won't be any form data in a GET request
        return render_template('get_city.html')


@app.route('/weather', methods=['POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        return get_weather(city)
    return render_template('get_city.html')


@app.route('/weather/<city>')
def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        return jsonify(weather_info)

    return jsonify({'error': 'City not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2224, debug=True)
