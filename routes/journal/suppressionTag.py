from flask import Blueprint, current_app, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Création du blueprint
suppressionTag = Blueprint("suppressionTag", __name__)

@suppressionTag.route("/suppressionTag", methods=["DELETE"])
def delete_tag():
    try:
        data = request.json
        tagNom = data.get('tagNom')
        collectionArg = data.get('collection')
        idTrade = data.get('idTrade')

        print(tagNom)
        print(collectionArg)
        print(idTrade)

        mongo = PyMongo(current_app)
        collection = mongo.db[collectionArg]
        
        document = collection.find_one({"_id": ObjectId(idTrade)})
        
        if document:
            if "tag" in document and tagNom in document["tag"]:
                collection.update_one(
                    {"_id": ObjectId(idTrade)},
                    {"$pull": {"tag": tagNom}}
                )
                return jsonify({"message": f"Tag '{tagNom}' a été supprimé"}), 200
            else:
                return jsonify({"error": "Tag not found for the given ID and name"}), 404
        else:
            return jsonify({"error": "Document not found"}), 404

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
