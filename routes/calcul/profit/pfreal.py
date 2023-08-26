from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

pfreal = Blueprint('pfreal', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@pfreal.route('/calculer_profit_factor_reel', methods=['GET'])
def calculate_pfreal(data):
    # Récupération des données du POST request
    data = request.get_json()
    username = data.get('username')

    # Récupération de la collection spécifique pour l'utilisateur
    user_collection = db[username + '_close']

    # Initialisation des totaux pondérés
    total_gain_pondere = 0
    total_perte_pondere = 0

    # Recherche de tous les trades pour cet utilisateur
    trades = user_collection.find({})

    for trade in trades:
        profit = trade.get('profit', 0)
        percent = trade.get('Percent', 1)  # si percent n'est pas présent, considérez-le comme 1 par défaut

        # Calculez le profit ou la perte pondérée basé sur le risque standard de 1%
        if profit > 0:
            total_gain_pondere += profit / percent 
        else:
            total_perte_pondere += abs(profit) / percent # Nous utilisons abs() pour s'assurer que la perte est positive

    # Évitons la division par zéro
    if total_perte_pondere == 0:
        profit_factor_reel = float('inf')  # signifie que nous avons seulement des gains, pas de pertes
    else:
        profit_factor_reel = total_gain_pondere / total_perte_pondere

    # Sauvegardons le résultat dans la collection 'username_unitaire'
    result_collection = db[username + '_unitaire']
    result_collection.update_one(
        {},  # cela mettra à jour le premier document trouvé, ou en insérera un nouveau si aucun document n'est trouvé
        {
            '$set': {
                'profit_factor_reel': profit_factor_reel,
                # ajoutez ici d'autres clés et valeurs si nécessaire
            }
        },
        upsert=True
    )

    return jsonify({'message': 'Profit factor réel calculé et sauvegardé avec succès', 'profit_factor_reel': profit_factor_reel})
