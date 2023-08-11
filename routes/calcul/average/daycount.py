from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

daycount = Blueprint('daycount', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']

@app.route('/daycount', methods=['POST'])  # I changed it to POST for passing username data safely
def calculate_daycount():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required!"}), 400

    collection_name = f"{username}_close"
    collection = db[collection_name]

    # Assuming that there's a 'date' field in each document which contains the date
    distinct_dates = collection.aggregate([
        {
            "$group": {
                "_id": "$date"
            }
        },
        {
            "$count": "distinctDateCount"
        }
    ])

    result = list(distinct_dates)
    if result:
        return result[0]['distinctDateCount']
    else:
        return 0

app.register_blueprint(daycount)

if __name__ == "__main__":
    app.run(debug=True)
