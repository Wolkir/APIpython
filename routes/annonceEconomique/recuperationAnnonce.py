from flask import Flask, Blueprint, current_app, jsonify
import schedule
import time
import threading
import requests

app = Flask(__name__)

recuperationAnnonce = Blueprint('recuperationAnnonce', __name)

def get_data_from_api():
    api_url = 'https://eodhd.com/api/economic-events?api_token=6530da188309e6.66620223'
    data = requests.get(api_url).json()
    print(data)
    return data

def schedule_weekly_task():
    schedule.every().monday.at("10:00").do(get_data_from_api)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/recuperationAnnonce', methods=['GET'])
def get_data():
    data = get_data_from_api()
    return jsonify(data)

@recuperationAnnonce.record
def setup_schedule(state):
    app = state.app
    if app:
        schedule_weekly_task()
        t = threading.Thread(target=run_schedule)
        t.daemon = True
        t.start()

if __name__ == '__main__':
    app.register_blueprint(recuperationAnnonce)
    app.run()
