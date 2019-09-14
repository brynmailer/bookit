from flask import request
from flask_restful import Resource
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from datetime import date, datetime
from database import db

class Payments(Resource):
    def get(self, project_id):
        # return all payments for the given project
        project = db.projects.find_one({'_id': ObjectId(project_id)})
        return dumps([payment for payment in db.payments.find({'_id': {'$in': project['payments']}})], json_options=RELAXED_JSON_OPTIONS), 200

    def post(self, project_id):
        # create new payment and return it
        payments = db.payments
        projects = db.projects
        req_body = request.get_json(force=True)
        payment_id = payments.insert_one({
            'amount': req_body['amount'],
            'date': datetime.strptime(req_body['date'], '%m/%d/%Y'),
            'status': req_body['status'],
            'description': req_body['description'],
        }).inserted_id
        projects.update_one({'_id': ObjectId(project_id)}, {'$set': {
            'payments': projects.find_one({'_id': ObjectId(project_id)})['payments'] + [ObjectId(payment_id)]
        }})
        return dumps(payments.find({'_id': ObjectId(payment_id)}), json_options=RELAXED_JSON_OPTIONS), 201
    
    def delete(self, project_id):
        # delete all payments from the given project
        project = db.projects.find_one({'_id': ObjectId(project_id)})
        db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': {
            'payments': []
        }})
        return f"{db.payments.delete_many({'_id': {'$in': project['payments']}}).deleted_count} payments deleted from project with id {project_id}", 200