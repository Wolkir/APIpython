from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime

weekday = Blueprint('weekday', __name__)

@weekday.route('/weekday', methods=['GET'])
def add_weekday():
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    documents = list(collection.find())

    for document in documents:
        date_string = document.get('dateAndTimeOpening', '')
        if isinstance(date_string, datetime):
            day = date_string.strftime('%A')
        else:
            date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
            day = date.strftime('%A')
            document['day'] = day

        collection.update_one({'_id': document['_id']}, {'$set': {'day': day}})

    client.close()

    return jsonify({'message': 'Weekday added successfully'})