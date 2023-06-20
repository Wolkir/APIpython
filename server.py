import sys

from pymongo import MongoClient
from flask import Flask

from routes.dateDuJour import dateDuJour
from routes.semaineGlissante import semaineGlissante
from routes.semaineEnCours import semaineEnCours
from routes.moisEnCours import moisEnCours
from routes.moisGlissant import moisGlissant
#from routes.Symbole import Symbole
from routes.RR import RR
from routes.Equity import Equity


app = Flask(__name__)
app.register_blueprint(dateDuJour)
app.register_blueprint(semaineGlissante)
app.register_blueprint(semaineEnCours)
app.register_blueprint(moisEnCours)
app.register_blueprint(moisGlissant)
#app.register_blueprint(Symbole)
app.register_blueprint(RR)
app.register_blueprint(Equity)

@app.route('/')
def hello_world():
    return '301sds37!'

if __name__ == '__main__':
    client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority")
    collection = client.db["things"]
    app.run()
