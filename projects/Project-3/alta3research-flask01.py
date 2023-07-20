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
    if request.method == 'POST':
        city = request.form['city']
        return get_weather(city)
    return render_template('get_city.html')


@app.route('/weather', methods=['GET', 'POST'])
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
    app.run(debug=True)
