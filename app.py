import datetime
import threading
from flask import Flask,jsonify
import sys
from apiworker import update_db
from grapher import update_graphs
from flask_apscheduler import APScheduler
from descriptor import make_descriptions

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
        },
        {
            'id': 'job2',
            'func': 'app:grapher_update',
            'args': (),
            'trigger': 'interval',
            'seconds': 86400  # Generate new graphs once a day
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


def grapher_update():
    log("Generating new graphs...")
    update_graphs()
    log("Finished generating graphs!")


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

if __name__ == "__main__":
    app.run()
