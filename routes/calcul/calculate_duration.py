from flask import Flask, Blueprint, jsonify
from datetime import datetime

calculate_duration = Blueprint('calculate_duration', __name__)

def calculate_time_duration(data):
    try:
        # Calculer la durée pour chaque document dans les données JSON
        for doc in data:
            opening_time = datetime.fromisoformat(doc['dateAndTimeOpening'])
            closure_time = datetime.fromisoformat(doc['dateAndTimeClosure'])
            
            # Calculer la durée
            duration = closure_time - opening_time
            doc['duration'] = str(duration)
        
        return data, 200
    except Exception as e:
        return {"error": str(e)}, 400

@calculate_duration.route('/calculate_duration', methods=['POST'])
def update_time_duration():
    try:
        data = request.json
        # Call the calculate_time_duration() function and pass the JSON data
        updated_data, status_code = calculate_time_duration(data)
        return jsonify(updated_data), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
