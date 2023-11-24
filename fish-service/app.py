import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify

app = Flask(__name__)

load_dotenv()


# Connection parameters
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USERNAME'),
        password=os.getenv('DATABASE_PASSWORD'),
        host='localhost'
    )
    return conn


# Get fish information by ID
@app.route('/fish/<fish_id>', methods=['GET'])
def get_fish_by_id(fish_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM fnd_animal_crossing.fish WHERE fish_id = %s', (fish_id,))
        fish = cursor.fetchone()
        cursor.close()
        conn.close()

        if fish is None:
            return jsonify({'error': 'Fish not found'}), 404

        # Database Schema
        fish_data = {
            'fish_id': fish[0],
            'name': fish[1],
            'sell': fish[2],
            'location': fish[3],
            'difficulty': fish[4],
            'size': fish[5],
            'vision': fish[6],
            'description': fish[7]
        }
        return jsonify(fish_data)

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
