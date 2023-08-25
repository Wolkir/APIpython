
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
        raise ValueError("No 'percent' value provided")
    
    try:
        percent_value = float(percent)
    except ValueError:
        raise ValueError("'percent' should be a number")
    
    # Comparaison de la valeur avec 1
    if percent_value > 1:
        overrisk = True
    else:
        overrisk = False
    
    return overrisk
