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

            # Assuming you have metadata associated with the image
            image_info = {
                'id': image.metadata['id'],
                'filename': image.metadata['filename'],
                # Add other image metadata fields here
            }
            image_info_list.append(image_info)

        response = app.response_class(
            response=image_data[0].getvalue(),
            content_type='image/jpeg'
        )

        return jsonify({'image_info': image_info_list, 'image_data': response.data})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

