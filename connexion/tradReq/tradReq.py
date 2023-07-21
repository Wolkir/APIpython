from flask import Flask, Blueprint, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

app = Flask(__name__)

trade_blueprint = Blueprint('trade', __name__)

def compare_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    closure_position = data.get('closurePosition')

    try:
        # Vérifier l'authentification de l'utilisateur
        user = db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Access denied"}), 401

        # Hacher le mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Récupérer la collection correspondant au nom d'utilisateur et closurePosition
        if closure_position == "Open":
            collection_name = f"{username}_open"
            user_collection = db[collection_name]

            # Vérifier si un ordre ouvert avec cet identifiant existe déjà
            existing_open_order = user_collection.find_one({"identifier": data.get('identifier'), "closurePosition": "Open"})

            if existing_open_order:
                # Mettre à jour le volume de l'ordre ouvert avec le nouveau volume
                existing_open_order['volume'] = data.get('volume')
                user_collection.replace_one({"_id": existing_open_order["_id"]}, existing_open_order)
            else:
                # Créer une nouvelle instance de TradeRequest pour l'ordre ouvert
                trade_request = {
                    "username": username,
                    "password": hashed_password,
                    "ticketNumber": data.get('ticketNumber'),
                    "identifier": data.get('identifier'),
                    "dateAndTimeOpening": data.get('dateAndTimeOpening'),
                    "typeOfTransaction": data.get('typeOfTransaction'),
                    "volume": data.get('volume'),
                    "symbol": data.get('symbole'),
                    "priceOpening": data.get('priceOpening'),
                    "stopLoss": data.get('stopLoss'),
                    "takeProfit": data.get('takeProfit'),
                    "closurePosition": closure_position
                }

                # Enregistrer l'objet dans la collection de l'utilisateur et closurePosition
                user_collection.insert_one(trade_request)
        else:
            # Si l'ordre est une demande de fermeture, nous devons vérifier s'il correspond à un ordre ouvert existant
            collection_name = f"{username}_open"
            user_collection = db[collection_name]

            existing_open_order = user_collection.find_one({"identifier": data.get('identifier'), "closurePosition": "Open"})

            if existing_open_order:
                # Mettre à jour le volume fermé pour l'ordre ouvert
                existing_open_order['volume_closed'] = existing_open_order.get('volume_closed', 0) + data.get('volume')

                # Vérifier si le volume fermé correspond au volume total de l'ordre ouvert
                if existing_open_order['volume_closed'] >= existing_open_order['volume']:
                    # Supprimer l'ordre ouvert de la collection des ordres ouverts
                    user_collection.delete_one({"_id": existing_open_order["_id"]})
                else:
                    # Mettre à jour l'ordre ouvert avec le nouveau volume fermé
                    user_collection.replace_one({"_id": existing_open_order["_id"]}, existing_open_order)
            else:
                # Si l'ordre ouvert n'existe pas, nous ne pouvons pas fermer cet ordre
                return jsonify({"message": "Open order not found"}), 404

        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')
