from flask import Blueprint, jsonify
from datetime import datetime

calculate_duration = Blueprint('calculate_duration', __name__)

def calculate_time_duration(data):
    try:
        # Calculate the duration for each data entry in the list
        for entry in data:
            opening_time = datetime.fromisoformat(entry['dateAndTimeOpening'])
            closure_time = datetime.fromisoformat(entry['dateAndTimeClosure'])
            duration = closure_time - opening_time
            entry['duration'] = str(duration)
        
        return jsonify({"message": "La clé 'durée' a été ajoutée aux données JSON"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
