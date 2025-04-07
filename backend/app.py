from flask import Flask, jsonify, request
from calculations import calculate_full_transfer
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Golf525 API!"})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    result = calculate_full_transfer(data)
    return jsonify(result)

@app.route('/locations', methods=['GET'])
def get_locations():
    with open('locations.json', 'r', encoding='utf-8') as file:
        locations = json.load(file)
    return jsonify(list(locations.keys()))

if __name__ == '__main__':
    app.run(debug=True)
