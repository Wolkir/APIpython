from flask import Flask, Blueprint, jsonify, request
from flask_pymongo import PyMongo
import bcrypt

# Création de l'application Flask
app = Flask(__name__)

# Configuration de la connexion MongoDB
app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)

trade_blueprint = Blueprint('trade', __name__)

def compare_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        # Connexion à la base de données MongoDB (déjà initialisé)
        global mongo  # Indiquer que l'on souhaite utiliser la variable 'mongo' globale

        # Vérifier l'authentification de l'utilisateur
        user = mongo.db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Authentification échouée"}), 401

        # Hacher le mot de passe avant de l'enregistrer dans la collection traderequests
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
            "symbole": data.get('symbole'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "takeProfit": data.get('takeProfit'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "commision": data.get('commision'), 
            "closurePosition": data.get('closurePosition'), 
            # Ajoutez ici les autres champs de la demande de transaction en fonction de vos besoins
        }

        # Enregistrer l'objet dans la base de données
        mongo.db.thingsTest.insert_one(trade_request)
        return jsonify({"message": "Données enregistrées avec succès"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint dans l'application Flask