from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour /sortiemanu
sortiemanu = Blueprint('sortiemanu', __name__)

@sortiemanu.route('/sortiemanu', methods=['GET'])
def calculate_sortiemanu(entry):


    username = entry.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
    
    closurePosition = entry.get('closurePosition')
    TPR = entry.get('TPR')
    SLR = entry.get('SLR')

    if closurePosition == 'Close' and TPR == False and SLR == False:
        Smanu = True
    else:
        Smanu = False

    return Smanu



