from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

pfreal = Blueprint('pfreal', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def calculate_pfreal(data):
    gains_pondere = 0
    pertes_pondere = 0

    for trans in data.get('transactions', []):
        profit = trans.get('profit', 0)
        percent = trans.get('percent', 1)
        if profit > 0:
            gains_pondere += profit * percent
        else:
            pertes_pondere += abs(profit) * percent

    if pertes_pondere == 0:
        return float('inf')
    return gains_pondere / pertes_pondere

@pfreal.route('/profit-factor-real', methods=['POST'])
def get_profit_factor_real():
    data = request.json
    username = data.get('username')
    
    # Si le nom d'utilisateur n'est pas fourni, retourner une erreur
    if not username:
        return jsonify({"error": "Le champ 'username' est requis"}), 400

    # Calculer le Profit Factor Réel
    result = calculate_pfreal(data)

    # Mettre à jour ou insérer dans la base de données
    collection_name = f"{username}_unitaire"
    user_collection = db[collection_name]
    user_collection.update_one(
        {"username": username},
        {"$set": {"profit_factor_real": result}},
        upsert=True
    )

    return jsonify({"profit_factor_real": result, "message": "Mis à jour avec succès"})

# Pour l'intégrer dans une application Flask
app = Flask(__name__)
app.register_blueprint(pfreal)

if __name__ == "__main__":
    app.run(debug=True)
