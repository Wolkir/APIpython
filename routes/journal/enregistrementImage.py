from flask import Blueprint, request, jsonify, current_app
import pymongo
from bson import ObjectId
import gridfs
import io


enregistrerImage = Blueprint('enregistrerImage', __name__)

@enregistrerImage.route('/enregistrerImage', methods=['POST'])
def enregistrer_image():
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'Aucune image trouvée dans la requête'}), 400

        image = request.files['image']

        db = current_app.config['MONGO_DB']
        fs = gridfs.GridFS(db)

        image_id = fs.put(image.stream, filename=image.filename)

        return jsonify({'message': 'Image enregistrée avec succès', 'image_id': str(image_id)})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500
