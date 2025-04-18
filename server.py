from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = 'location_data.json'

def save_location(lat, lng):
    with open(DATA_FILE, 'w') as f:
        json.dump({"latitude": lat, "longitude": lng}, f)

def load_location():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"latitude": None, "longitude": None}

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    lat, lng = data.get('latitude'), data.get('longitude')
    if lat and lng:
        save_location(lat, lng)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 400

@app.route('/get_location', methods=['GET'])
def get_location():
    return jsonify(load_location())

@app.route('/')
def home():
    location = load_location()
    return render_template('map.html', **location)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)