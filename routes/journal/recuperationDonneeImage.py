from flask import Blueprint, current_app, request, Flask, jsonify
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

recuperationDonneeImage = Blueprint('recuperationDonneeImage', __name__)

@recuperationDonneeImage.route('/recuperationDonneeImage', methods=['GET'])
def recuperation_image():
    try:
        image_id = request.args.get('imageId', None)
        app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority'
        mongo = MongoClient(app.config['MONGO_URI'])
        db = mongo["test"]
        fs = gridfs.GridFS(db)

        images = fs.find({'metadata.id': image_id})
        if images.count() == 0:
            return jsonify({'message': 'Aucune image trouvée'}), 404

        image_ids = []  # Liste pour stocker les _id des images

        for image in images:
            image_ids.append(str(image._id))  # Convertissez l'ObjectId en chaîne si nécessaire

        return jsonify({'image_ids': image_ids})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500
