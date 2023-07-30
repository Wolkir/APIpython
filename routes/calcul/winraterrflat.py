from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
winrrt = Blueprint('winrrt', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']
collection_unitaire = db['unitaire']

@winrrt.route('/winrrt', methods=['GET'])
def calculate_winrrt():
    # Récupérer la valeur de winrate de la collection "unitaire"
    winrate = collection_unitaire.find_one({}, {"winrate": 1})["winrate"]

    # Récupérer la valeur de risk_reward de la collection "unitaire"
    risk_reward = collection_unitaire.find_one({}, {"RR": 1})["RR"]

    # Calculer RRT
    RRT = ((1 - (winrate/100)) / (winrate/100))

    # Calculer WinrateT
    WinrateT = (1 / (1 + risk_reward))*100

    # Ajouter les valeurs calculées à la collection "unitaire"
    collection_unitaire.update_one({}, {"$set": {"RRFlat": RRT, "WinrateFlat": WinrateT}}, upsert=True)

