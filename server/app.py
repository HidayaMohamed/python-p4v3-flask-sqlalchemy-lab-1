#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ------------------------
# Basic views
# ------------------------

@app.route('/')
def index():
    return "<h1>Python Operations with Flask Routing and Views</h1>"

@app.route('/print/<parameter>')
def print_string(parameter):
    print(parameter)
    return parameter

@app.route('/count/<parameter>')
def count(parameter):
    parameter = int(parameter)
    return "\n".join(str(i) for i in range(parameter)) + "\n"

@app.route('/math/<num1>/<operation>/<num2>')
def math(num1, operation, num2):
    num1 = int(num1)
    num2 = int(num2)

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "div":
        result = num1 / num2
    elif operation == "%":
        result = num1 % num2
    else:
        return "Invalid operation"

    return str(result)

# ------------------------
# Earthquake routes
# ------------------------

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter_by(magnitude=magnitude).all()
    if earthquakes:
        return make_response(jsonify([eq.to_dict() for eq in earthquakes]), 200)
    else:
        return make_response(
            jsonify({"message": f"No earthquakes found with magnitude {magnitude}."}),
            404
        )

# ------------------------
# Prepopulate database for testing
# ------------------------

with app.app_context():
    db.create_all()
    if not Earthquake.query.first():
        eq1 = Earthquake(id=1, magnitude=9.5, location="Chile", year=1960)
        eq2 = Earthquake(id=2, magnitude=9.2, location="Alaska", year=1964)
        eq3 = Earthquake(id=3, magnitude=9.5, location="Japan", year=2011)
        db.session.add_all([eq1, eq2, eq3])
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
