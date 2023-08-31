import json
import os

from flask import request, jsonify


class NameServer:

    def __init__(self, app, type='names'):
        self.app = app
        self.type = type

    def get_name_file(self):
        p = os.path.join('~', '.takephoto', self.type)
        return os.path.expanduser(p)

    def get_names(self, server):
        names = {}
        full_path = self.get_name_file()
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                names = json.load(f)
        if server in names:
            return names[server]
        return names

    def save_names(self, data):
        if not self.allow_server(data['server']):
            return
        full_path = self.get_name_file()
        names = {}
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                names = json.load(f)
        names[data['server']] = data

        with open(full_path, 'w') as f:
            f.write(json.dumps(names))
        self.app.logger.info(f"write names[{data['server']}] to {full_path}")

    def allow_server(self, server):
        return server in ['login', 'tcp']


def define_controller(app):
    @app.route('/name')
    def name():
        server = request.args.get('server')
        name_server = NameServer(app=app)
        if not name_server.allow_server(server):
            return jsonify({})
        ret = name_server.get_names(server)
        return jsonify(ret)

    @app.route('/name', methods=['PUT'])
    def write_name():
        data = request.json
        if 'server' not in data:
            return 'OK'
        name_server = NameServer(app=app)
        name_server.save_names(data)
        return 'OK'
