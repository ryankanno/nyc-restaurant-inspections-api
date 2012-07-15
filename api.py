from flask import Flask, request
app = Flask(__name__)

from database import db_session

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET'])
def search():
    name = request.args.get('name', '', type=str)
    address = request.args.get('address', '', type=str)

    if name and address:
        return "{0}-{1}".format(name, address)
    else:
        val = name or address
        return "{0}".format(val)


if __name__ == "__main__":
    app.run(debug=True)
