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

def handle_close_transaction(username, data):
    # Récupérer la collection correspondant aux positions ouvertes de l'utilisateur
    open_collection = db[f"{username}_open"]

    # Chercher si une position ouverte avec le même identifier et volume existe
    existing_position = open_collection.find_one({
        "identifier": data.get('identifier'),
        "volume": data.get('volume'),
    })

    if existing_position:
        # S'il y a une position ouverte avec le même identifier et volume
        if existing_position['volume'] == data.get('volume'):
            # Supprimer la position ouverte
            open_collection.delete_one({"_id": existing_position["_id"]})
        else:
            # La position ouverte doit être mise à jour avec le nouveau volume
            updated_volume = existing_position['volume'] - data.get('volume')
            open_collection.update_one(
                {"_id": existing_position["_id"]},
                {"$set": {"volume": updated_volume}}
            )

    # Récupérer la collection correspondant aux positions fermées de l'utilisateur
    close_collection = db[f"{username}_close"]

    # Chercher si une position fermée avec le même identifier existe
    existing_close_position = close_collection.find_one({
        "identifier": data.get('identifier'),
    })

    if existing_close_position:
        # Une position fermée avec le même identifier existe
        # Ajouter le volume à la position existante
        updated_volume = existing_close_position['volume'] + data.get('volume')
        close_collection.update_one(
            {"_id": existing_close_position["_id"]},
            {"$set": {"volume": updated_volume}}
        )
    else:
        # Aucune position fermée avec le même identifier, créer une nouvelle
        trade_request = {
            "username": username,
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
            "balance": data.get('balance'),
            "broker": data.get('broker')
            # Ajoutez ici les autres champs de la demande de transaction en fonction de vos besoins
        }
        close_collection.insert_one(trade_request)

# Route pour enregistrer une transaction
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

        if closure_position == "Open":
            # Construire le nom de la collection pour les positions ouvertes
            collection_name = f"{username}_open"
            # Récupérer la collection correspondant aux positions ouvertes de l'utilisateur
            user_collection = db[collection_name]

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
                "closurePosition": closure_position,
                "balance": data.get('balance'),
                "broker": data.get('broker')
                # Ajoutez ici les autres champs de la demande de transaction en fonction de vos besoins
            }

            # Enregistrer l'objet dans la collection de l'utilisateur et closurePosition
            user_collection.insert_one(trade_request)

        elif closure_position == "Close":
            handle_close_transaction(username, data)

        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
