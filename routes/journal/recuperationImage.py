from flask import Blueprint, jsonify, send_file, current_app, request
from pymongo import MongoClient
from flask import Flask
from bson import ObjectId
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

        image = fs.get(ObjectId(image_id))
        if image is None:
            return jsonify({'message': 'Image non trouvée'}), 500

        return send_file(io.BytesIO(image.read()), mimetype='image/jpeg')
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500
