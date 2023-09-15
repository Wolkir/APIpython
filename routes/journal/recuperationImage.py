from flask import Blueprint, jsonify, Flask, request
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
            return jsonify({'message': 'Aucune image trouvée'}), 404

        image_data = []

        for image in images:
            image_data.append({'_id': str(image._id), 'url': image['metadata']['url']})

        return jsonify(image_data)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

