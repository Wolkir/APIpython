from flask import Blueprint, request, jsonify, current_app, Flask
from pymongo import MongoClient
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
        id_value = request.form.get('id')
        collection_value = request.form.get('collection')

        print(id_value)
        print(collection_value)

        app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority'
        mongo = MongoClient(app.config['MONGO_URI'])
        db = mongo["test"]
        fs = gridfs.GridFS(db)

        metadata = {'id': id_value, 'collection': collection_value}

        print(metadata)

        # Récupération des images existantes avec le même id_value
        existing_images = list(fs.find({'metadata.id': id_value}))

        # Calcul du nombre total d'images après l'ajout
        total_images = len(existing_images) + 1

        if total_images > 3:
            return jsonify({'message': 'Il ne peut y avoir que 3 images par trade'}), 400

        # Enregistrement de l'image
        image_id = fs.put(image.stream, filename=image.filename, metadata=metadata)

        return jsonify({'message': 'Image enregistrée avec succès', 'image_id': str(image_id)})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500
