from flask import Flask, render_template, request, jsonify
from weather_tracker import WeatherTracker
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# 預設城市列表
CITIES = ['Taipei', 'Kaohsiung', 'Taichung']

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city', 'Taipei')
    tracker = WeatherTracker()
    weather_info = tracker.get_weather(city)
    
    if isinstance(weather_info, dict):
        return jsonify({
            'success': True,
            'data': weather_info
        })
    else:
        return jsonify({
            'success': False,
            'error': weather_info
        })

if __name__ == '__main__':
    app.run(debug=True) 