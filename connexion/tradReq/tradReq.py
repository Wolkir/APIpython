from flask import Flask, Blueprint, jsonify, request
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

        # Construire le nom de la collection en fonction de closurePosition
        collection_name = f"{username}_open" if closure_position == "Open" else f"{username}_close"

        # Récupérer la collection correspondant au nom d'utilisateur et closurePosition
        user_collection = db[collection_name]

        # Si l'ordre est une demande de fermeture
        if closure_position == "Close":
            identifier = data.get('identifier')
            volume = data.get('volume')

            # Rechercher l'ordre ouvert correspondant dans la collection des ordres ouverts
            open_order = user_collection.find_one({"identifier": identifier, "closurePosition": "Open"})

            if open_order:
                # Mettre à jour le volume fermé de l'ordre ouvert
                open_order['volume_closed'] = open_order.get('volume_closed', 0) + volume

                if open_order['volume_closed'] >= open_order['volume']:
                    # L'ordre ouvert est entièrement fermé, donc nous l'enregistrons dans la collection des ordres fermés
                    user_collection.delete_one({"identifier": identifier, "closurePosition": "Open"})

                    # Enregistrer l'ordre fermé dans la collection des ordres fermés
                    collection_name_close = f"{username}_close"
                    user_collection_close = db[collection_name_close]
                    user_collection_close.insert_one(open_order)
                else:
                    # Mettre à jour l'ordre ouvert avec le nouveau volume fermé
                    user_collection.replace_one({"_id": open_order["_id"]}, open_order)
            else:
                # Si l'ordre ouvert n'existe pas, nous ne pouvons pas fermer cet ordre
                return jsonify({"message": "Open order not found"}), 404

        else:
            # Si l'ordre est une demande d'ouverture, créer une nouvelle instance de TradeRequest
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
                "balance": data.get('balance')
                # Ajoutez ici les autres champs de la demande de transaction en fonction de vos besoins
            }

            # Enregistrer l'objet dans la collection de l'utilisateur et closurePosition
            user_collection.insert_one(trade_request)

        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')
