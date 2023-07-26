from flask import Blueprint, jsonify
from datetime import datetime

calculate_duration = Blueprint('calculate_duration', __name__)

def calculate_time_duration(data):
    try:
        # Calculate the duration between opening_time and closure_time
        opening_time = datetime.strptime(data['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")
        closure_time = datetime.strptime(data['dateAndTimeClosure'], "%Y-%m-%dT%H:%M:%S.%f%z")
        duration = closure_time - opening_time

        # Add the duration to the data dictionary
        data['duration'] = str(duration)

        return data  # Return the data dictionary with the 'duration' added
    except Exception as e:
        return {"error": str(e)}  # Return an error response if an exception occurs
