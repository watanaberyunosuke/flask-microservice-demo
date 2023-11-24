import os

import requests
from flask import Flask, jsonify, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# Get fish by ID from database
@app.route('/fish/<fish_id>', methods=['GET'])
def fish_by_fish_id(fish_id):
    try:
        response = requests.get('http://localhost:8081/fish/' + str(fish_id))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    if response.headers['Content-Type'] == 'application/json':
        return jsonify(response.json()), response.status_code
    else:
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = os.getenv('FLASK_PORT', '8080')
    app.run(host=host, port=int(port))
