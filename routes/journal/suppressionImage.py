from flask import Flask, Blueprint, request, current_app, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import gridfs

suppressionImage = Blueprint('suppressionImage', __name__)

@suppressionImage.route('/suppressionImage', methods=['DELETE'])
def delete_document():
    try:
        document_id = request.args.get('id')
        
        if not document_id:
            return jsonify({'error': 'ID not provided'}), 400
        
        mongo = PyMongo(current_app)
        db = mongo.db
        
        fs = gridfs.GridFS(db)
        
        fs.delete(ObjectId(document_id))
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
