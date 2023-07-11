from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

average_duration = Blueprint('average_duration', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@average_duration.route('/average_duration', methods=['GET'])
def calculate_average_duration():
    # Récupérer les documents avec les durées
    documents = collection.find()
    
    # Initialiser les variables
    total_duration = timedelta()
    document_count = 0
    
    # Calculer la durée totale et le nombre de documents
    for doc in documents:
        if 'durée' in doc:
            duration_str = doc['durée']
            duration_parts = duration_str.split(':')
            duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]), seconds=int(duration_parts[2]))
            total_duration += duration
            document_count += 1
    
    # Calculer la durée moyenne
    average_duration = total_duration / document_count if document_count > 0 else timedelta()
    
    # Insérer la durée moyenne dans la collection "unitaire"
    unitaire_collection = db['unitaire']
    unitaire_collection.update_one({}, {'$set': {'average_duration': str(average_duration)}}, upsert=True)
    
    return jsonify({"average_duration": str(average_duration)})