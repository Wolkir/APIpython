
from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

overrisk = Blueprint('overrisk', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def find_overrisk(data):
    # Assurez-vous que 'percent' est dans les données et qu'il s'agit d'un nombre
    percent = data.get('percent', None)
    
    if percent is None:
        return jsonify({"error": "No 'percent' value provided"}), 400
    
    try:
        percent_value = float(percent)
    except ValueError:
        return jsonify({"error": "'percent' should be a number"}), 400
    
    # Comparaison de la valeur avec 1
    if percent_value > 1:
        return jsonify({"overrisk": True})
    else:
        return jsonify({"overrisk": False})
