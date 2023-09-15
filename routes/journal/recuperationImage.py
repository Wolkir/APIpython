from flask import Blueprint, jsonify, Flask
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

recuperationImage = Blueprint('recuperationImage', __name__)

@recuperationImage.route('/recuperationImage', methods=['GET'])
def recuperation_image():
    try:
        image_id = request.args.get('imageId', None)
        app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority'
        mongo = MongoClient(app.config['MONGO_URI'])
        db = mongo["test"]
        fs = gridfs.GridFS(db)

        images = fs.find({'metadata.id': image_id})
        if images.count() == 0:
            print(images)
            return jsonify({'message': 'Aucune image trouvée'}), 404

        image_data = []
        image_ids = []  # Liste pour stocker les _id des images
        image_urls = []  # Liste pour stocker les URL des images

        for image in images:
            image_data.append(image.read())
            image_ids.append(str(image._id))  # Convertissez l'ObjectId en chaîne si nécessaire
            image_urls.append(image['metadata']['url'])  # Supposons que l'URL de l'image est stockée dans les métadonnées

        # Renvoyez les données sous forme de JSON
        response_data = [{'_id': id, 'url': url} for id, url in zip(image_ids, image_urls)]
        return jsonify(response_data)
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500


