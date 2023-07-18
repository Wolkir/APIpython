# auth_routes.py
from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import jwt

user = Blueprint('user', __name__)

def setup_user_routes(app):
    app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
    mongo = PyMongo(app)

    def create_collection(username):
        try:
            db = mongo.db
            db.create_collection(username)

            print('La collection a été créée avec succès.')
        except Exception as e:
            print('Erreur lors de la création de la collection :', e)

    @user.route('/signup', methods=['POST'])
    def signup():
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        create_collection(username)

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = {
                "username": username,
                "email": email,
                "password": hashed_password
            }
            mongo.db.users.insert_one(user)

            return jsonify({"message": "Utilisateur créé !"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @user.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        try:
            user = mongo.db.users.find_one({"email": email})
            if not user:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401

            hashed_password = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                token = jwt.encode({"userId": str(user['_id'])}, 'RANDOM_TOKEN_SECRET', algorithm='HS256').decode('utf-8')
                return jsonify({"userId": str(user['_id']), "token": token}), 200
            else:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @user.route('/users/<userId>', methods=['GET'])
    def get_user(userId):
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(userId)})
            if not user:
                return jsonify({"message": "Utilisateur non trouvé"}), 404

            user.pop("password", None)
            return jsonify({"user": user}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
