from flask import request
from flask_restful import Resource
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from datetime import date, datetime
from database import db

class Project(Resource):
    def get(self, project_id):
        # return project with parsed project_id
        return dumps(db.projects.find_one({'_id': ObjectId(project_id)}), json_options=RELAXED_JSON_OPTIONS)

    def put(self, project_id):
        # update project with parsed project_id
        projects = db.projects
        req_body = request.get_json(force=True)
        projects.update_one({'_id': ObjectId(project_id)}, {'$set': {
            'cost': req_body['cost'],
            'balance': req_body['cost'],
            'start': datetime.strptime(req_body['start'], '%m/%d/%Y'),
            'end': datetime.strptime(req_body['end'], '%m/%d/%Y'),
            'employer': req_body['employer'],
            'description': req_body['description']
        }})
        return dumps(projects.find({'_id': ObjectId(project_id)}), json_options=RELAXED_JSON_OPTIONS), 200
    
    def delete(self, project_id):
        # delete project with parsed project_id
        return f"Project with id {project_id} deleted" if db.projects.delete_one({'_id': ObjectId(project_id)}).deleted_count > 0 else f"No project with id {project_id}"