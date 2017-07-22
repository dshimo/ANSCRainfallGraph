import datetime
import threading
from flask import Flask, jsonify
import fcntl
import sys
from apiworker import update_db
from grapher import plot_vals, grapher_lock
from models import GageHeight, DischargeRate
from flask_apscheduler import APScheduler
from descriptor import make_descriptions
import base64
import os

app = Flask(__name__)
app.days = 10
logger_lock = threading.Lock()


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:apiworker_update',
            'args': (),
            'trigger': 'interval',
            'seconds': 3600  # Update the database once an hour
        },
        {
            'id': 'job2',
            'func': 'app:grapher_update',
            'args': (),
            'trigger': 'interval',
            'seconds': 3600  # Draw new graphs once an hour
        }
    ]


def log(string):
    with logger_lock:
        log = open('log.txt', 'w')
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


def grapher_update():
    log("Generating graphs...")
    plot_vals(GageHeight, app.days)
    plot_vals(DischargeRate, app.days)
    log("Finished generating graphs!")


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
if not os.path.exists("./gen"):
    os.makedirs("./gen")


@app.route("/")
def hello():
    return app.send_static_file('main.html')


@app.route("/descriptor")
def descriptor():
    d = make_descriptions()
    return jsonify(d)


@app.route("/graph/<graph_type>/<int:days>")
def generate_graph(graph_type, days):
    app.days = days
    filename = "./gen/" + graph_type + ".png"
    with grapher_lock:
        with open(filename, 'rb') as img:
            data = img.read()
            return base64.b64encode(data)

if __name__ == "__main__":
    os.chdir(os.path.expanduser('~') + '/src/ANSCRainfallGraph/')
    pid_file = 'program.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        print("another instance running, exiting...")
        sys.exit(0)
    app.run()
