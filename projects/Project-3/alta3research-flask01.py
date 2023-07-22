"""
Flask Weather App

This Flask app provides a simple weather information service using the OpenWeatherMap API.
Users can input a city name, and the app will retrieve and display the current weather data,
including temperature in Celsius and Fahrenheit, and a weather description.

Endpoints:
1. /: Main route to input a city name and get weather information.
2. /weather: Alternate route to get weather information using a POST request.
3. /weather/<city>: Retrieves weather information for the specified city.

Dependencies:
- Flask: A micro web framework for Python.
- requests: Library to make HTTP requests to the OpenWeatherMap API.
- dotenv: Library to load environment variables from a .env file.

Note:
This app requires a valid OpenWeatherMap API key stored as 'OPENWEATHERMAP_API_KEY' in a .env file.

Usage:
Run the app and visit 'http://localhost:2224/' in your web browser to access the weather service.
"""

from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Parse a .env file and then load all the variables found as environment variables.

# Hidden API key
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']  # Get the 'city' data from the submitted form
        return get_weather(city)  # Call the get_weather() function with the 'city' data and return the result
    else:
        return render_template('get_city.html')  # Render the 'get_city.html' template for the form


@app.route('/weather', methods=['POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']  # Get the 'city' data from the submitted form
        return get_weather(city)  # Call the get_weather() function with the 'city' data and return the result
    return render_template('get_city.html')  # Render the 'get_city.html' template for the form


@app.route('/weather/<city>')
def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}  # Set up parameters for the API request
    response = requests.get(BASE_URL, params=params)  # Make a GET request to the OpenWeatherMap API

    if response.status_code == 200:  # If the API request is successful
        data = response.json()  # Get the JSON data from the response
        weather_info = {
            'city': data['name'],  # Extract city name from the data
            'temperature': {
                'fahrenheit': (data['main']['temp'] * 9 / 5) + 32,  # Convert temperature to Fahrenheit
                'celsius': data['main']['temp']  # Temperature in Celsius
            },
            'description': data['weather'][0]['description']  # Get the weather description
        }
        return jsonify(weather_info)  # Return the weather information as JSON response

    return jsonify({'error': 'City not found'}), 404  # Return error response if city is not found


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2224, debug=True)  # Start the Flask server on host and port, with debugging enabled
