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

        image_data = []
        image_info_list = []

        for image in images:
            image_data.append(io.BytesIO(image.read()))

            # Récupérez l'_id directement de l'objet image
            image_info = {
                '_id': str(image._id)
            }
            image_info_list.append(image_info)

        response = app.response_class(
            response=image_data[0].getvalue(),
            content_type='image/jpeg'
        )

        return jsonify({'infos_image': image_info_list, 'donnees_image': response.data})
    except Exception as e:
        current_app.logger.error(f"Une erreur s'est produite : {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

