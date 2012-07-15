from flask import Flask, request, jsonify
from database import db_session

import sys, os
PROJECT_ROOT = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from models import Action

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET'])
def search():
    name = request.args.get('name', '', type=str)
    address = request.args.get('address', '', type=str)
    return jsonify(actions=[(action.code, action.description) for action in Action.query.all()])


if __name__ == "__main__":
    app.run(debug=True)
