from flask import Blueprint, Flask, request, send_file
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

        image = fs.find_one({'metadata.id': image_id})
        if image is None:
            return jsonify({'message': 'Aucune image trouvée'}), 404

        image_data = image.read()
        return send_file(io.BytesIO(image_data), mimetype='image/jpeg')

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

if __name__ == "__main__":
    app.register_blueprint(recuperationImage)
    app.run()

