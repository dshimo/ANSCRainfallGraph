import datetime
import threading
from flask import Flask, jsonify
import sys
from apiworker import update_db
from grapher import plot_vals
from models import GageHeight, DischargeRate
from flask_apscheduler import APScheduler
from descriptor import make_descriptions
import base64

app = Flask(__name__)
logger_lock = threading.Lock()


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:apiworker_update',
            'args': (),
            'trigger': 'interval',
            'seconds': 3600  # Update the database once an hour
        }
    ]


def log(string):
    with logger_lock:
        log = open('log.txt', 'a')
        now = datetime.datetime.now()
        print(str(now), end=": ", file=sys.stderr)
        print(string, file=sys.stderr)
        print(str(now), end=": ", file=log)
        print(string, file=log)
        log.close()


def apiworker_update():
    log("Updating database...")
    update_db(1)
    log("Finished updating database!")


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route("/")
def hello():
    return app.send_static_file('main.html')


@app.route("/descriptor")
def descriptor():
    d = make_descriptions()
    return jsonify(d)


@app.route("/graph/<graph_type>/<int:days>")
def generate_graph(graph_type, days):
    if graph_type == "GageHeight":
        plot_vals(GageHeight, days)
    elif graph_type == "DischargeRate":
        plot_vals(DischargeRate, days)
    filename = "./gen/" + graph_type + ".png"
    with open(filename, 'rb') as img:
        data = img.read()
        return base64.b64encode(data)

if __name__ == "__main__":
    app.run()
