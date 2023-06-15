from flask import Flask
from routes.nom import nom
from routes.dateSeul import dateSeul
from routes.semaineGlissante import semaineGlissante
from routes.semaineEnCours import semaineEnCours
from routes.moisEnCours import moisEnCours
from routes.moisGlissant import moisGlissant

app = Flask(__name__)

app.register_blueprint(nom)
app.register_blueprint(dateSeul)
app.register_blueprint(semaineGlissante)
app.register_blueprint(semaineEnCours)
app.register_blueprint(moisEnCours)
app.register_blueprint(moisGlissant)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
