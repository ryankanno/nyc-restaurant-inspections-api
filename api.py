from flask import Flask, request, jsonify
from database import db_session

import sys, os
PROJECT_ROOT = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from models import Restaurant

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET'])
def search():
    results = []
    name = request.args.get('name', '', type=str)
    restaurants = Restaurant.query.filter(Restaurant.name.like("%{0}%".format(name.upper())))

    for restaurant in restaurants:
        i = []
        for inspection in restaurant.inspections:
            
            inspect = {
                'current_grade': inspection.current_grade,
                'inspected_date': inspection.graded_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'score': inspection.score,
            }

            if inspection.action:
                inspect['action_code'] = inspection.action.code
                inspect['action_desc'] = inspection.action.description

            if inspection.violation:
                inspect['violation_code'] = inspection.violation.code
                inspect['violation_desc'] = inspection.violation.description

            i.append(inspect)

        i.sort(key=lambda x:x['inspected_date'], reverse=True)
        r = restaurant.to_json
        r['inspections'] = i
        results.append(r)

    return jsonify(data=results)


if __name__ == "__main__":
    app.run(debug=True)
