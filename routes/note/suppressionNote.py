from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['Note']

suppressionNote = Blueprint('suppressionNote', __name__)

@suppressionNote.route('/suppressionNote', methods=['DELETE'])
def delete_note():
    note_id = request.args.get('id')
    if note_id:
        try:
            result = collection.delete_one({'_id': ObjectId(note_id)})
            if result.deleted_count > 0:
                return jsonify({'message': 'Note supprimée avec succès'})
            else:
                return jsonify({'error': 'Note introuvable'})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Paramètre "id" manquant'})
