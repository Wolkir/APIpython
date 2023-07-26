from flask import Blueprint, jsonify
from datetime import datetime

calculate_duration = Blueprint('calculate_duration', __name__)

def calculate_time_duration(data):
    try:
        # Calculate the duration for each data entry in the list
        for entry in data:
            opening_time = datetime.strptime(entry['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")
            closure_time = datetime.strptime(entry['dateAndTimeClosure'], "%Y-%m-%dT%H:%M:%S.%f%z")
            duration = closure_time - opening_time
            entry['duration'] = str(duration)
        
        return data  # Return the entire 'data' list with the 'duration' added to each element
    except Exception as e:
        return {"error": str(e)}  # Return an error response if an exception occurs
