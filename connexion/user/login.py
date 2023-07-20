from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
import jwt

login_blueprint = Blueprint('login', __name__)

def setup_login_routes(app):
    @login_blueprint.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        try:
            # Connexion à la base de données MongoDB
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)

            # Recherche de l'utilisateur dans la collection users
            user = mongo.db.users.find_one({"email": email})
            if not user:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401

            # Vérification du mot de passe haché
            hashed_password = user['password']  # Le mot de passe est déjà stocké sous forme de bytes
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                # Génération du jeton d'authentification
                token = jwt.encode({"userId": str(user['_id'])}, 'RANDOM_TOKEN_SECRET', algorithm='HS256')
                return jsonify({"userId": str(user['_id']), "token": token}), 200
            else:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return login_blueprint
