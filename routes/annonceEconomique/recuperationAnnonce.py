from flask import Flask, Blueprint, current_app
import schedule
import time
import requests

recuperationAnnonce = Blueprint('recuperationAnnonce', __name__)

def get_data_from_api():
    api_url = 'https://eodhd.com/api/economic-events?api_token=6530da188309e6.66620223'
    data = requests.get(api_url).json()
    print(data)

def schedule_weekly_task():
    schedule.every().monday.at("10:00").do(get_data_from_api)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@weekly_task.record
def setup_schedule(state):
    app = state.app
    if app:
        schedule_weekly_task()
        import threading
        t = threading.Thread(target=run_schedule)
        t.daemon = True
        t.start()
