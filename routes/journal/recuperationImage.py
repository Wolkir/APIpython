from flask import Blueprint, send_file, current_app, request, jsonify, Flask
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
            print(images)
            return jsonify({'message': 'Aucune image trouvée'}), 404

        image_data = []
        image_ids = []  # Liste pour stocker les _id des images

        for image in images:
            image_data.append(image.read())
            image_ids.append(str(image._id))  # Convertissez l'ObjectId en chaîne si nécessaire

        response = send_file(io.BytesIO(b''.join(image_data)), mimetype='image/jpeg')
        
        # Ajoutez le champ _id à la réponse JSON
        response.headers['image_id'] = ','.join(image_ids)

        return response
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

