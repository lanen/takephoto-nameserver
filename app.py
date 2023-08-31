from flask import Flask, jsonify

from logging.config import dictConfig
from nameserver.route import define_controller

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

static_dir = 'static'

app = Flask(__name__, static_url_path="", static_folder='static-local')

define_controller(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run()