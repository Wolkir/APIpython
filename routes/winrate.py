from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
winrate = Blueprint('winrate', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['collection']
collection = db['things']

@winrate.route('/winrate', methods=['GET'])
def calculate_winrate():
    # Compter le nombre de documents avec profit > 0
    positive_profits_count = collection.count_documents({"profit": {"$gt": 0}})
    
    # Compter le nombre de documents avec profit < 0
    negative_profits_count = collection.count_documents({"profit": {"$lt": 0}})
    
    # Calcul du winrate
    winrate = positive_profits_count / (positive_profits_count + negative_profits_count) * 100
    
    # Fermeture de la connexion à la base de données
    client.close()
    
    # Retourne le résultat du calcul du winrate au format JSON
    return jsonify({"winrate": winrate})

app.register_blueprint(winrate)

if __name__ == '__main__':
    app.run()
