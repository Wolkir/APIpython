from flask import Flask, Blueprint, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

app = Flask(__name__)

trade_blueprint = Blueprint('trade', __name__)

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

        # Construire le nom de la collection en fonction de closurePosition
        collection_name = f"{username}_open" if closure_position == "Open" else f"{username}_close"

        # Récupérer la collection correspondant au nom d'utilisateur et closurePosition
        user_collection = db[collection_name]

        # Chercher si une position ouverte avec le même identifier et volume existe
        existing_position = None
        if closure_position == "Close":
            existing_position = user_collection.find_one({
                "identifier": data.get('identifier'),
                "volume": data.get('volume'),
            })

        if existing_position:
            # S'il y a une position ouverte avec le même identifier et volume
            if existing_position['volume'] == data.get('volume'):
                # Supprimer la position ouverte
                user_collection.delete_one({"_id": existing_position["_id"]})
            else:
                # La position ouverte doit être mise à jour avec le nouveau volume
                updated_volume = existing_position['volume'] - data.get('volume')
                user_collection.update_one(
                    {"_id": existing_position["_id"]},
                    {"$set": {"volume": updated_volume}}
                )

        # Créer une nouvelle instance de TradeRequest à partir des données reçues
        trade_request = {
            "username": username,
            "password": hashed_password,
            "ticketNumber": data.get('ticketNumber'),
            "identifier": data.get('identifier'),
            "magicNumber": data.get('magicNumber'),
            "dateAndTimeOpening": data.get('dateAndTimeOpening'),
            "typeOfTransaction": data.get('typeOfTransaction'),
            "volume": data.get('volume'),
            "symbol": data.get('symbole'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "takeProfit": data.get('takeProfit'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "commission": data.get('commision'),
            "closurePosition": closure_position,
            "balance": data.get('balance'),
            "broker": data.get('broker')
            # Ajoutez ici les autres champs de la demande de transaction en fonction de vos besoins
        }

        # Enregistrer l'objet dans la collection de l'utilisateur et closurePosition
        user_collection.insert_one(trade_request)
        return jsonify({"message": "Data saved successfully Python CLOSE"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
