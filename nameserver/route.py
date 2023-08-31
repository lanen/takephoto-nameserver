import json
import os

from flask import request, jsonify


def allow_server(server):
    return server in ['login', 'tcp']


def define_controller(app):
    @app.route('/name')
    def name():
        server = request.args.get('server')
        if not allow_server(server):
            return jsonify({})
        full_path = os.path.expanduser('~/.takephoto/names')
        names = {}
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                names = json.load(f)
        if server in names:
            return jsonify(names[server])
        return jsonify({})

    @app.route('/name', methods=['PUT'])
    def write_name():
        data = request.json()
        if not 'server' in data:
            return jsonify({})
        if not allow_server(data['server']):
            return jsonify({})
        full_path = os.path.expanduser('~/.takephoto/names')

        names = {}
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                names = json.load(f)
        names[data['server']] = data

        with open(full_path, 'w') as f:
            f.write(json.dumps(names))
        return 'OK'
