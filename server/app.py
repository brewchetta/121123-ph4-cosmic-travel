#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


# SCIENTISTS ROUTES #

@app.get('/scientists')
def get_all_scientists():
    all_scientists = Scientist.query.all()
    return [ scientist.to_dict( rules=("-missions",) ) for scientist in all_scientists  ], 200

@app.get('/scientists/<int:id>')
def get_scientist_by_id(id):
    found_scientist = Scientist.query.where(Scientist.id == id).first()
    if found_scientist:
        return found_scientist.to_dict(), 200
    else:
        return { "error": "Lost in space" }, 404

@app.post('/scientists')
def hire_scientist():
    data = request.json

    try:
        new_scientist = Scientist(name=data.get('name'), field_of_study=data.get('field_of_study'))
        db.session.add(new_scientist)
        db.session.commit()
        return new_scientist.to_dict(), 201

    except ValueError as error:
        return { "errors": f"{error}" }, 400

@app.patch('/scientists/<int:id>')
def update_scientist(id):
    data = request.json
    found_scientist = Scientist.query.where(Scientist.id == id).first()

    if found_scientist:
        try:
            for key in data:
                setattr(found_scientist, key, data[key])
            db.session.commit()
            return found_scientist.to_dict(), 202

        except ValueError as error:
            return { "errors": f"{error}" }, 400

    else:
        return { "error": "Houston we have a problem" }, 404
    
@app.delete('/scientists/<int:id>')
def delete_scientist(id):
    found_scientist = Scientist.query.where(Scientist.id == id).first()
    if found_scientist:
        db.session.delete(found_scientist)
        db.session.commit()
        return {}, 204
    else:
        return { "error": "Scientist already lost in space" }, 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
