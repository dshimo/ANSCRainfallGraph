from flask import Flask
import sys
from apiworker import update_db
from grapher import update_graphs
from flask_apscheduler import APScheduler

app = Flask(__name__)


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


def apiworker_update():
    print("Updating database...", file=sys.stderr)
    update_db(1)
    print("Finished updating database!", file=sys.stderr)


def grapher_update():
    print("Generating new graphs...", file=sys.stderr)
    update_graphs()
    print("Finished generating graphs!!", file=sys.stderr)


@app.route("/")
def hello():
    return app.send_static_file('main.html')

if __name__ == "__main__":
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run()
