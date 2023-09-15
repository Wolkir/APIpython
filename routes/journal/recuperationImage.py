from flask import Blueprint, Flask, request, send_file, jsonify
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

recuperationImage = Blueprint('recuperationImage', __name__)

@recuperationImage.route('/recuperationImage', methods=['GET'])
def recuperation_image():
    try:
        image_id = request.args.get('imageId', None)

        # Connexion à la base de données MongoDB
        client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
        db = client["test"]
        fs = gridfs.GridFS(db)

        # Recherche de l'image par ID
        image = fs.find_one({'metadata.id': image_id})

        if image is None:
            return jsonify({'message': 'Aucune image trouvée'}), 404

        # Renvoyer l'image en tant que fichier téléchargeable
        response = send_file(
            image, 
            mimetype='image/jpeg',
            as_attachment=True,  # Permet le téléchargement
            attachment_filename=f'image_{image_id}.jpg'  # Nom du fichier à télécharger
        )
        return response

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

if __name__ == "__main__":
    app.register_blueprint(recuperationImage)
    app.run(debug=True)

