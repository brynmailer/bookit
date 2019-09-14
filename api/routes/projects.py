from flask import request
from flask_restful import Resource
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from datetime import date, datetime
from database import db

class Projects(Resource):
    def get(self):
        # return all projects
        return dumps([project for project in db.projects.find()], json_options=RELAXED_JSON_OPTIONS), 200

    def post(self):
        # create new project and return it
        projects = db.projects
        req_body = request.get_json(force=True)
        project_id = projects.insert_one({
            'cost': req_body['cost'],
            'balance': req_body['cost'],
            'start': datetime.strptime(req_body['start'], '%m/%d/%Y'),
            'end': datetime.strptime(req_body['end'], '%m/%d/%Y'),
            'employer': req_body['employer'],
            'description': req_body['description'],
            'payments': [],
            'log': []
        })
        return dumps(projects.find({'_id': ObjectId(project_id)}), json_options=RELAXED_JSON_OPTIONS), 201
    
    def delete(self):
        return f"{db.projects.delete_many({}).deleted_count} projects deleted", 200


