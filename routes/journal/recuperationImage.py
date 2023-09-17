from flask import Blueprint, Flask, request, jsonify, send_file
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

recuperationImage = Blueprint('recuperationImage', __name__)

@app.route('/recuperationImage', methods=['GET'])
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

        # Créez une liste pour stocker les données JSON des images
        image_data_list = []

        # Parcourez les images et ajoutez leurs données à la liste
        for image in images:
            image_url = f'/image/{image["_id"]}'
            image_data_list.append({
                'image_id': str(image["_id"]),
                'image_url': image_url
            })

        # Renvoyez la liste des données JSON (toutes les images correspondantes)
        return jsonify(image_data_list)

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'message': f'Une erreur est survenue : {str(e)}'}), 500

if __name__ == "__main__":
    app.register_blueprint(recuperationImage)
    app.run(debug=True)

    app.run(debug=True)


