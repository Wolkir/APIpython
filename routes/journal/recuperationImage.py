from flask import Blueprint, jsonify, send_file, current_app, request, Flask
from pymongo import MongoClient
import gridfs
import io

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

        image_info_list = []

        for image in images:
            # Récupérez l'_id directement de l'objet image
            image_info = {
                '_id': str(image._id)
                'image_url': f'https://https://apipython2.onrender.com/recuperationImage?imageId={str(image._id)}'
            }
            image_info_list.append(image_info)

        return jsonify({'infos_image': image_info_list})
    except Exception as e:
        current_app.logger.error(f"Une erreur s'est produite : {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

