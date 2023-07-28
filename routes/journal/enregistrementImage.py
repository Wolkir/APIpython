from flask import Blueprint, request, jsonify, current_app, Flask
import pymongo
from bson import ObjectId
import gridfs
import io

app = Flask(__name__)

enregistrerImage = Blueprint('enregistrerImage', __name__)

@enregistrerImage.route('/enregistrerImage', methods=['POST'])
def enregistrer_image():
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'Aucune image trouvée dans la requête'}), 400

        image = request.files['image']

        app.config['MONGO_URI'] = 'mongodb://localhost:27017/nom_de_votre_base_de_donnees'
        mongo = MongoClient(app.config['MONGO_URI'])
        fs = gridfs.GridFS(mongo)

        image_id = fs.put(image.stream, filename=image.filename)

        return jsonify({'message': 'Image enregistrée avec succès', 'image_id': str(image_id)})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500
