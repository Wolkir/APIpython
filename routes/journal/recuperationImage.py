from flask import Blueprint, Flask, request, send_file, jsonify
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

recuperationImage = Blueprint('recuperationImage', __name__)

@recuperationImage.route('/recuperationImage', methods=['GET'])
def recuperation_images():
    try:
        image_id = request.args.get('imageId', None)

        # Connexion à la base de données MongoDB
        client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
        db = client["test"]
        fs = gridfs.GridFS(db)

        # Recherche de toutes les images correspondant à la condition
        images = fs.find({'metadata.id': image_id})

        if images.count() == 0:
            return jsonify({'message': 'Aucune image trouvée'}), 404

        # Créez une liste pour stocker les réponses
        responses = []

        # Parcourez les images et ajoutez-les à la liste de réponses
        for image in images:
            response = send_file(
                image, 
                mimetype='image/jpeg',
                as_attachment=True,  # Permet le téléchargement
                attachment_filename=f'image_{image_id}.jpg'  # Nom du fichier à télécharger
            )
            responses.append(response)

        # Renvoyer la liste de réponses (toutes les images correspondantes)
        return responses

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

if __name__ == "__main__":
    app.register_blueprint(recuperationImage)
    app.run(debug=True)

